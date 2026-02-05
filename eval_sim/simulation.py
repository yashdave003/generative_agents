"""
Evaluation Ecosystem Simulation

Main simulation loop for studying competition dynamics between model providers
and the effects of Goodhart's law on benchmark validity.

Key visibility design:
- Simulation holds ground truth externally in ground_truth dict
- Actors only have access to public_state and private_state
- Ground truth is passed to evaluator for scoring, never to actors
"""
import json
import os
from dataclasses import dataclass, field, asdict
from typing import Optional

from actors.model_provider import ModelProvider
from actors.evaluator import Evaluator, Regulation
from visibility import ProviderGroundTruth, ConsumerGroundTruth, PolicymakerGroundTruth, FunderGroundTruth


@dataclass
class SimulationConfig:
    """Configuration for a simulation run."""
    # Simulation parameters
    n_rounds: int = 50
    seed: Optional[int] = 42

    # Evaluator/Benchmark parameters (single benchmark mode)
    benchmark_name: str = "capability_benchmark"
    benchmark_validity: float = 0.7  # alpha
    benchmark_exploitability: float = 0.5  # beta
    benchmark_noise: float = 0.1  # sigma

    # Multi-benchmark mode (if provided, overrides single benchmark params)
    # Each dict should have: name, validity, exploitability, noise_level, weight
    benchmarks: Optional[list] = None

    # Provider parameters
    rnd_efficiency: float = 0.01  # How much R&D improves true capability per round

    # Planning mode
    llm_mode: bool = False  # If True, use LLM for planning; if False, use heuristics

    # New actor settings
    enable_consumers: bool = False  # Enable consumer actors
    enable_policymakers: bool = False  # Enable policymaker actors
    enable_funders: bool = False  # Enable funder actors
    n_consumers: int = 10  # Number of consumer actors
    n_policymakers: int = 1  # Number of policymaker actors
    n_funders: int = 1  # Number of funder actors

    # Output
    output_dir: Optional[str] = None
    verbose: bool = True

    def to_dict(self) -> dict:
        """Convert config to dict for serialization."""
        d = asdict(self)
        # Handle benchmarks list specially since it may contain dicts
        if self.benchmarks:
            d["benchmarks"] = self.benchmarks
        return d


class EvalEcosystemSimulation:
    """
    Main simulation class for the evaluation ecosystem.

    Simulates rounds of:
    1. Providers choose strategies (R&D vs gaming allocation)
    2. Providers' true capabilities update based on R&D
    3. Evaluator scores all providers
    4. Scores are published
    5. Providers observe scores and update beliefs
    6. Consumers observe leaderboard and make subscription decisions
    7. Policymakers observe ecosystem and may issue regulations

    Key visibility design:
    - ground_truth dict holds all invisible state (true_capability, true_satisfaction, etc.)
    - Actors only access their own public_state and private_state
    - Ground truth is passed to evaluator and used for computing actual outcomes
    """

    def __init__(self, config: SimulationConfig):
        self.config = config
        self.providers: list[ModelProvider] = []
        self.consumers: list = []  # Will be Consumer instances
        self.policymakers: list = []  # Will be Policymaker instances
        self.funders: list = []  # Will be Funder instances
        self.evaluator: Optional[Evaluator] = None
        self.current_round: int = 0
        self.history: list[dict] = []

        # Ground truth held externally by simulation
        # Format: {actor_name: GroundTruth}
        self.ground_truth: dict = {}

        # Funder data for current round (used for funding multipliers)
        self._current_funder_data: dict = {}

    def setup(
        self,
        provider_configs: list[dict],
        evaluator: Optional[Evaluator] = None,
        consumer_configs: list[dict] = None,
        policymaker_configs: list[dict] = None,
        funder_configs: list[dict] = None,
    ):
        """
        Initialize the simulation with providers and evaluator.

        Args:
            provider_configs: List of dicts with provider initialization params.
                Each dict should have: name, strategy_profile, innate_traits,
                initial_capability, initial_believed_capability (optional),
                initial_strategy (optional dict with investment allocations)
            evaluator: Optional pre-configured Evaluator. If None, creates one
                from config.
            consumer_configs: Optional list of consumer configurations
            policymaker_configs: Optional list of policymaker configurations
        """
        # Create providers and their ground truth
        self.providers = []
        for pc in provider_configs:
            provider = ModelProvider(
                name=pc["name"],
                strategy_profile=pc["strategy_profile"],
                innate_traits=pc["innate_traits"],
                initial_capability=pc.get("initial_capability", 0.5),
                initial_believed_capability=pc.get("initial_believed_capability"),
                initial_believed_exploitability=pc.get("initial_believed_exploitability", 0.3),
                llm_mode=self.config.llm_mode,
                verbose_llm=pc.get("verbose_llm", False),
            )

            # Apply initial strategy if provided
            if "initial_strategy" in pc:
                strategy = pc["initial_strategy"]
                provider.private_state.fundamental_research = strategy.get("fundamental_research", 0.25)
                provider.private_state.training_optimization = strategy.get("training_optimization", 0.25)
                provider.private_state.evaluation_engineering = strategy.get("evaluation_engineering", 0.25)
                provider.private_state.safety_alignment = strategy.get("safety_alignment", 0.25)
                # Sync with legacy scratch
                provider.scratch.fundamental_research = provider.private_state.fundamental_research
                provider.scratch.training_optimization = provider.private_state.training_optimization
                provider.scratch.evaluation_engineering = provider.private_state.evaluation_engineering
                provider.scratch.safety_alignment = provider.private_state.safety_alignment

            self.providers.append(provider)

            # Initialize ground truth externally
            self.ground_truth[provider.name] = ProviderGroundTruth(
                true_capability=pc.get("initial_capability", 0.5)
            )

        # Create consumers if enabled
        if self.config.enable_consumers:
            self._setup_consumers(consumer_configs)

        # Create policymakers if enabled
        if self.config.enable_policymakers:
            self._setup_policymakers(policymaker_configs)

        # Create funders if enabled
        if self.config.enable_funders:
            self._setup_funders(funder_configs)

        # Create or use provided evaluator
        if evaluator is not None:
            self.evaluator = evaluator
        elif self.config.benchmarks:
            # Multi-benchmark mode
            self.evaluator = Evaluator(
                benchmarks=self.config.benchmarks,
                seed=self.config.seed,
            )
        else:
            # Single benchmark mode
            self.evaluator = Evaluator(
                benchmark_name=self.config.benchmark_name,
                validity=self.config.benchmark_validity,
                exploitability=self.config.benchmark_exploitability,
                noise_level=self.config.benchmark_noise,
                seed=self.config.seed,
            )

        self.current_round = 0
        self.history = []

        if self.config.verbose:
            print("=== Simulation Setup ===")
            print(f"Providers: {[p.name for p in self.providers]}")
            if self.consumers:
                print(f"Consumers: {len(self.consumers)}")
            if self.policymakers:
                print(f"Policymakers: {len(self.policymakers)}")
            if self.funders:
                print(f"Funders: {[f.name for f in self.funders]}")
            print(self.evaluator.get_benchmark_summary())
            print()

    def _setup_consumers(self, consumer_configs: list[dict] = None):
        """Set up consumer actors."""
        try:
            from actors.consumer import Consumer
        except ImportError:
            if self.config.verbose:
                print("Consumer actor not available yet")
            return

        if consumer_configs is None:
            # Create default consumers
            consumer_configs = [
                {"name": f"Consumer_{i}", "use_cases": ["general"]}
                for i in range(self.config.n_consumers)
            ]

        for cc in consumer_configs:
            consumer = Consumer(
                name=cc["name"],
                use_cases=cc.get("use_cases", ["general"]),
                budget=cc.get("budget", 100.0),
                quality_sensitivity=cc.get("quality_sensitivity", 0.5),
            )
            self.consumers.append(consumer)

            # Initialize consumer ground truth
            self.ground_truth[consumer.name] = ConsumerGroundTruth(
                true_satisfaction=0.5,
                true_quality_sensitivity=cc.get("quality_sensitivity", 0.5),
            )

    def _setup_policymakers(self, policymaker_configs: list[dict] = None):
        """Set up policymaker actors."""
        try:
            from actors.policymaker import Policymaker
        except ImportError:
            if self.config.verbose:
                print("Policymaker actor not available yet")
            return

        if policymaker_configs is None:
            # Create default policymaker
            policymaker_configs = [
                {
                    "name": "Regulator",
                    "policy_objectives": ["safety", "fairness"],
                    "intervention_threshold": 0.3,
                }
            ]

        for pc in policymaker_configs:
            policymaker = Policymaker(
                name=pc["name"],
                policy_objectives=pc.get("policy_objectives", ["safety"]),
                intervention_threshold=pc.get("intervention_threshold", 0.3),
            )
            self.policymakers.append(policymaker)

            # Initialize policymaker ground truth
            self.ground_truth[policymaker.name] = PolicymakerGroundTruth(
                true_risk_tolerance=pc.get("risk_tolerance", 0.5),
                true_intervention_effectiveness=pc.get("intervention_effectiveness", 0.5),
            )

    def _setup_funders(self, funder_configs: list[dict] = None):
        """Set up funder actors."""
        try:
            from actors.funder import Funder, get_default_funder_configs
        except ImportError:
            if self.config.verbose:
                print("Funder actor not available yet")
            return

        if funder_configs is None:
            # Use default funder configs
            funder_configs = get_default_funder_configs()[:self.config.n_funders]

        for fc in funder_configs:
            funder = Funder(
                name=fc["name"],
                funder_type=fc.get("funder_type", "vc"),
                total_capital=fc.get("total_capital", 1000000.0),
                risk_tolerance=fc.get("risk_tolerance", 0.5),
                mission_statement=fc.get("mission_statement", ""),
                llm_mode=self.config.llm_mode,
            )
            self.funders.append(funder)

            # Initialize funder ground truth
            self.ground_truth[funder.name] = FunderGroundTruth(
                true_roi=0.0,
                funding_efficiency=fc.get("funding_efficiency", 1.0),
            )

    def _update_ground_truth(self, provider_name: str, capability_gain: float):
        """
        Update ground truth for a provider after R&D execution.

        Args:
            provider_name: Name of the provider
            capability_gain: How much true capability increased
        """
        if provider_name in self.ground_truth:
            gt = self.ground_truth[provider_name]
            if isinstance(gt, ProviderGroundTruth):
                gt.true_capability += capability_gain

    def _sync_provider_ground_truth(self, provider: ModelProvider):
        """
        Sync provider's internal state with external ground truth.

        For backwards compatibility, we keep provider.scratch.true_capability
        in sync with external ground truth.
        """
        if provider.name in self.ground_truth:
            gt = self.ground_truth[provider.name]
            if isinstance(gt, ProviderGroundTruth):
                provider.scratch.true_capability = gt.true_capability

    def run_round(self) -> dict:
        """
        Run a single simulation round.

        Updated flow:
        1. Providers plan and execute (R&D updates capability with funding multiplier)
        2. Evaluator scores all providers using ground truth
        3. Scores are published
        4. Providers observe and reflect
        5. Consumers observe leaderboard and decide subscriptions
        6. Policymakers observe and may intervene
        7. Funders observe and allocate funding
        8. Record round data

        Returns:
            Dict with round results
        """
        round_num = self.current_round

        # Get funding multipliers from previous round's funder decisions
        funding_multipliers = self._current_funder_data.get("funding_multipliers", {})

        # 1. Providers plan investment portfolios (for round > 0, they've seen previous scores)
        if round_num > 0:
            for provider in self.providers:
                portfolio = provider.plan()

                # Calculate capability gain based on portfolio
                # Different investments contribute differently to capability
                base_efficiency = self.config.rnd_efficiency

                # Apply funding multiplier (1.0 if no funding, up to 2.0 with max funding)
                funding_multiplier = funding_multipliers.get(provider.name, 1.0)
                effective_efficiency = base_efficiency * funding_multiplier

                capability_gain = (
                    portfolio["fundamental_research"] * effective_efficiency * 1.5 +  # High variance, high ceiling
                    portfolio["training_optimization"] * effective_efficiency * 1.0 +  # Moderate, reliable
                    portfolio["evaluation_engineering"] * effective_efficiency * 0.1   # Minimal capability gain
                    # Safety alignment doesn't directly improve capability
                )

                # Update external ground truth
                self._update_ground_truth(provider.name, capability_gain)

                # Sync for backwards compatibility
                self._sync_provider_ground_truth(provider)

                # Record execution in provider memory
                provider.memory.append({
                    "type": "execution",
                    "round": round_num,
                    "capability_gain": capability_gain,
                    "funding_multiplier": funding_multiplier,
                    "new_true_capability": self.ground_truth[provider.name].true_capability,
                    "portfolio": portfolio,
                })

        # 2. Evaluator scores all providers using ground truth
        scores = self.evaluator.evaluate_all(
            self.providers,
            round_num,
            ground_truth=self.ground_truth,
        )

        # 3. Publish scores
        published_scores = self.evaluator.publish_scores(scores)
        leaderboard = self.evaluator.get_leaderboard(scores)

        # 4. Providers observe scores and reflect
        for provider in self.providers:
            own_score = published_scores[provider.name]
            competitor_scores = {
                name: score
                for name, score in published_scores.items()
                if name != provider.name
            }
            provider.observe(own_score, competitor_scores, round_num)
            provider.reflect()

        # 5. Consumer actions (if enabled)
        consumer_data = {}
        if self.consumers:
            consumer_data = self._run_consumer_round(leaderboard, round_num)

        # 6. Policymaker actions (if enabled)
        policymaker_data = {}
        if self.policymakers:
            policymaker_data = self._run_policymaker_round(
                leaderboard, consumer_data, round_num
            )

        # 7. Funder actions (if enabled)
        funder_data = {}
        if self.funders:
            funder_data = self._run_funder_round(
                leaderboard, consumer_data, policymaker_data, round_num
            )
            # Store for next round's capability gain calculation
            self._current_funder_data = funder_data

        # Record round data
        round_data = {
            "round": round_num,
            "scores": dict(scores),  # Composite scores
            "true_capabilities": {
                p.name: self.ground_truth[p.name].true_capability
                for p in self.providers
            },
            "believed_capabilities": {
                p.name: p.private_state.believed_own_capability
                for p in self.providers
            },
            "strategies": {
                p.name: {
                    "fundamental_research": p.fundamental_research,
                    "training_optimization": p.training_optimization,
                    "evaluation_engineering": p.evaluation_engineering,
                    "safety_alignment": p.safety_alignment,
                }
                for p in self.providers
            },
            "leaderboard": leaderboard,
        }

        # Add per-benchmark scores if multiple benchmarks
        if len(self.evaluator.benchmarks) > 1:
            round_data["per_benchmark_scores"] = self.evaluator.get_per_benchmark_scores(round_num)
            round_data["benchmark_names"] = [bm.name for bm in self.evaluator.benchmarks]

        # Add consumer data if present
        if consumer_data:
            round_data["consumer_data"] = consumer_data

        # Add policymaker data if present
        if policymaker_data:
            round_data["policymaker_data"] = policymaker_data

        # Add funder data if present
        if funder_data:
            round_data["funder_data"] = funder_data

        self.history.append(round_data)

        if self.config.verbose:
            self._print_round_summary(round_data)

        self.current_round += 1
        return round_data

    def _run_consumer_round(self, leaderboard: list, round_num: int) -> dict:
        """
        Run consumer actions for the round.

        Args:
            leaderboard: Current leaderboard [(name, score), ...]
            round_num: Current round number

        Returns:
            Dict with consumer data for this round
        """
        try:
            from actors.consumer import Consumer
        except ImportError:
            return {}

        consumer_data = {
            "subscriptions": {},
            "satisfaction": {},
            "switches": 0,
        }

        for consumer in self.consumers:
            if not isinstance(consumer, Consumer):
                continue

            # Consumer observes leaderboard
            consumer.observe(leaderboard, round_num)

            # Consumer reflects on experience
            consumer.reflect()

            # Consumer plans subscription decision
            old_subscription = consumer.private_state.current_subscription
            consumer.plan()

            # Consumer executes subscription
            consumer.execute()

            # Track switches
            new_subscription = consumer.private_state.current_subscription
            if old_subscription != new_subscription:
                consumer_data["switches"] += 1

            # Compute actual satisfaction based on ground truth
            if new_subscription and new_subscription in self.ground_truth:
                provider_gt = self.ground_truth[new_subscription]
                if isinstance(provider_gt, ProviderGroundTruth):
                    # Satisfaction based on true capability vs expectations
                    consumer_gt = self.ground_truth.get(consumer.name)
                    if isinstance(consumer_gt, ConsumerGroundTruth):
                        # True satisfaction = how well model serves consumer
                        believed_quality = consumer.private_state.believed_model_quality.get(
                            new_subscription, 0.5
                        )
                        true_satisfaction = provider_gt.true_capability
                        # Dissatisfaction if true capability < believed quality
                        consumer_gt.true_satisfaction = true_satisfaction

            consumer_data["subscriptions"][consumer.name] = new_subscription
            consumer_gt = self.ground_truth.get(consumer.name)
            if isinstance(consumer_gt, ConsumerGroundTruth):
                consumer_data["satisfaction"][consumer.name] = consumer_gt.true_satisfaction

        # Aggregate statistics
        satisfactions = list(consumer_data["satisfaction"].values())
        if satisfactions:
            consumer_data["avg_satisfaction"] = sum(satisfactions) / len(satisfactions)
            consumer_data["min_satisfaction"] = min(satisfactions)

        return consumer_data

    def _run_policymaker_round(
        self,
        leaderboard: list,
        consumer_data: dict,
        round_num: int,
    ) -> dict:
        """
        Run policymaker actions for the round.

        Args:
            leaderboard: Current leaderboard
            consumer_data: Consumer data from this round
            round_num: Current round number

        Returns:
            Dict with policymaker data for this round
        """
        try:
            from actors.policymaker import Policymaker
        except ImportError:
            return {}

        policymaker_data = {
            "interventions": [],
            "active_regulations": [],
        }

        for policymaker in self.policymakers:
            if not isinstance(policymaker, Policymaker):
                continue

            # Policymaker observes ecosystem state
            policymaker.observe(
                leaderboard=leaderboard,
                consumer_satisfaction=consumer_data.get("avg_satisfaction"),
                validity_correlation=self.evaluator.compute_validity_correlation(),
                round_num=round_num,
            )

            # Policymaker reflects on observations
            policymaker.reflect()

            # Policymaker plans intervention
            intervention = policymaker.plan()

            # Policymaker executes intervention
            if intervention:
                policymaker.execute(intervention)

                # Apply intervention to evaluator
                if intervention.get("type") == "mandate_benchmark":
                    regulation = Regulation(
                        name=intervention.get("name", f"Regulation_{round_num}"),
                        regulation_type="mandate_benchmark",
                        details=intervention.get("details", {}),
                        issued_round=round_num,
                        active=True,
                    )
                    self.evaluator.add_regulation(regulation)

                policymaker_data["interventions"].append({
                    "policymaker": policymaker.name,
                    "type": intervention.get("type"),
                    "details": intervention.get("details"),
                })

        # Record active regulations
        policymaker_data["active_regulations"] = [
            r.get_summary() for r in self.evaluator.get_active_regulations()
        ]

        return policymaker_data

    def _run_funder_round(
        self,
        leaderboard: list,
        consumer_data: dict,
        policymaker_data: dict,
        round_num: int,
    ) -> dict:
        """
        Run funder actions for the round.

        Args:
            leaderboard: Current leaderboard
            consumer_data: Consumer data from this round
            policymaker_data: Policymaker data from this round
            round_num: Current round number

        Returns:
            Dict with funder data for this round
        """
        try:
            from actors.funder import Funder
        except ImportError:
            return {}

        funder_data = {
            "allocations": {},
            "funding_multipliers": {},
            "total_funding": 0.0,
        }

        all_allocations = {}

        for funder in self.funders:
            if not isinstance(funder, Funder):
                continue

            # Funder observes ecosystem state (public signals only)
            funder.observe(
                leaderboard=leaderboard,
                consumer_data=consumer_data,
                policymaker_data=policymaker_data,
                round_num=round_num,
            )

            # Funder reflects on observations
            funder.reflect()

            # Funder plans funding allocations
            allocations = funder.plan()

            # Funder executes allocations
            funder.execute(allocations)

            # Record allocations
            funder_data["allocations"][funder.name] = allocations

            # Aggregate allocations per provider across all funders
            for provider_name, amount in allocations.items():
                if provider_name not in all_allocations:
                    all_allocations[provider_name] = 0.0
                all_allocations[provider_name] += amount

        # Calculate funding multipliers per provider
        # Multiplier based on total funding received relative to available capital
        total_available = sum(f.private_state.total_capital for f in self.funders)
        if total_available > 0:
            for provider_name, total_funding in all_allocations.items():
                # Proportion of total capital allocated to this provider
                proportion = total_funding / total_available
                # Multiplier: 1.0 (no funding) to 2.0 (all capital)
                multiplier = 1.0 + min(1.0, proportion)
                funder_data["funding_multipliers"][provider_name] = multiplier

        funder_data["total_funding"] = sum(all_allocations.values())

        return funder_data

    def run(self, n_rounds: Optional[int] = None) -> list[dict]:
        """
        Run the full simulation.

        Args:
            n_rounds: Number of rounds to run. If None, uses config.n_rounds.

        Returns:
            List of round data dicts
        """
        if n_rounds is None:
            n_rounds = self.config.n_rounds

        if self.config.verbose:
            print(f"=== Running {n_rounds} rounds ===\n")

        for _ in range(n_rounds):
            self.run_round()

        if self.config.verbose:
            self._print_final_summary()

        return self.history

    def _print_round_summary(self, round_data: dict):
        """Print a summary of a round."""
        print(f"--- Round {round_data['round']} ---")
        print("Leaderboard:")
        for rank, (name, score) in enumerate(round_data["leaderboard"], 1):
            true_cap = round_data["true_capabilities"][name]
            believed_cap = round_data["believed_capabilities"][name]
            strategy = round_data["strategies"][name]
            print(
                f"  {rank}. {name}: score={score:.3f} "
                f"(true={true_cap:.3f}, believed={believed_cap:.3f}) "
                f"[R:{strategy['fundamental_research']:.0%} T:{strategy['training_optimization']:.0%} "
                f"E:{strategy['evaluation_engineering']:.0%} S:{strategy['safety_alignment']:.0%}]"
            )

        # Print consumer summary if present
        if "consumer_data" in round_data:
            cd = round_data["consumer_data"]
            if "avg_satisfaction" in cd:
                print(f"  Consumer Satisfaction: {cd['avg_satisfaction']:.2f} avg, {cd['switches']} switches")

        # Print policymaker summary if present
        if "policymaker_data" in round_data:
            pd = round_data["policymaker_data"]
            if pd.get("interventions"):
                for intervention in pd["interventions"]:
                    print(f"  [REGULATION] {intervention['policymaker']}: {intervention['type']}")

        # Print funder summary if present
        if "funder_data" in round_data:
            fd = round_data["funder_data"]
            if fd.get("funding_multipliers"):
                multipliers = fd["funding_multipliers"]
                multiplier_strs = [f"{p}:{m:.2f}x" for p, m in multipliers.items()]
                print(f"  [FUNDING] Multipliers: {', '.join(multiplier_strs)}")

        print()

    def _print_final_summary(self):
        """Print final simulation summary."""
        print("=== Simulation Complete ===")
        print()

        # Final leaderboard
        if self.history:
            final = self.history[-1]
            print("Final Standings:")
            for rank, (name, score) in enumerate(final["leaderboard"], 1):
                true_cap = final["true_capabilities"][name]
                print(f"  {rank}. {name}: score={score:.3f}, true_capability={true_cap:.3f}")

        # Validity correlation
        correlation = self.evaluator.compute_validity_correlation()
        if correlation is not None:
            print(f"\nBenchmark validity correlation: {correlation:.3f}")
            if correlation < 0.5:
                print("  [!] Low correlation suggests benchmark gaming may be distorting scores")

        # Strategy evolution
        print("\nInvestment Evolution (first -> last round):")
        for provider in self.providers:
            if len(provider.private_state.past_strategies) >= 2:
                first = provider.private_state.past_strategies[0]
                last = provider.private_state.past_strategies[-1]
                if isinstance(first, dict) and isinstance(last, dict):
                    print(
                        f"  {provider.name}: "
                        f"Research {first.get('fundamental_research', 0):.0%}->{last.get('fundamental_research', 0):.0%}, "
                        f"Training {first.get('training_optimization', 0):.0%}->{last.get('training_optimization', 0):.0%}, "
                        f"EvalEng {first.get('evaluation_engineering', 0):.0%}->{last.get('evaluation_engineering', 0):.0%}, "
                        f"Safety {first.get('safety_alignment', 0):.0%}->{last.get('safety_alignment', 0):.0%}"
                    )

        # Consumer summary if present
        if self.consumers and self.history:
            final = self.history[-1]
            if "consumer_data" in final:
                cd = final["consumer_data"]
                print(f"\nFinal Consumer State:")
                print(f"  Average Satisfaction: {cd.get('avg_satisfaction', 'N/A'):.2f}")
                total_switches = sum(
                    h.get("consumer_data", {}).get("switches", 0)
                    for h in self.history
                )
                print(f"  Total Subscription Switches: {total_switches}")

        # Funder summary if present
        if self.funders and self.history:
            final = self.history[-1]
            if "funder_data" in final:
                fd = final["funder_data"]
                print(f"\nFinal Funder State:")
                print(f"  Total Funding Deployed: ${fd.get('total_funding', 0):,.0f}")
                if fd.get("funding_multipliers"):
                    print("  Final Funding Multipliers:")
                    for provider, mult in fd["funding_multipliers"].items():
                        print(f"    {provider}: {mult:.2f}x")

    def save(self, output_dir: Optional[str] = None):
        """Save simulation state and history."""
        if output_dir is None:
            output_dir = self.config.output_dir
        if output_dir is None:
            output_dir = "./simulation_output"

        os.makedirs(output_dir, exist_ok=True)

        # Save config
        with open(f"{output_dir}/config.json", "w") as f:
            json.dump(self.config.to_dict(), f, indent=2)

        # Save history
        with open(f"{output_dir}/history.json", "w") as f:
            json.dump(self.history, f, indent=2)

        # Save ground truth
        ground_truth_data = {}
        for name, gt in self.ground_truth.items():
            ground_truth_data[name] = gt.to_dict()
        with open(f"{output_dir}/ground_truth.json", "w") as f:
            json.dump(ground_truth_data, f, indent=2)

        # Save evaluator
        self.evaluator.save(f"{output_dir}/evaluator.json")

        # Save providers
        providers_dir = f"{output_dir}/providers"
        os.makedirs(providers_dir, exist_ok=True)
        for provider in self.providers:
            provider.save(f"{providers_dir}/{provider.name}")

        if self.config.verbose:
            print(f"\nSimulation saved to: {output_dir}")

    def get_analysis_data(self) -> dict:
        """
        Extract data in a format suitable for analysis/plotting.

        Returns:
            Dict with arrays for easy plotting
        """
        rounds = [h["round"] for h in self.history]

        data = {
            "rounds": rounds,
            "providers": {},
        }

        for provider in self.providers:
            name = provider.name
            data["providers"][name] = {
                "scores": [h["scores"][name] for h in self.history],
                "true_capabilities": [h["true_capabilities"][name] for h in self.history],
                "believed_capabilities": [h["believed_capabilities"][name] for h in self.history],
                "rnd_investment": [h["strategies"][name]["rnd"] for h in self.history],
                "gaming_investment": [h["strategies"][name]["gaming"] for h in self.history],
            }

        # Add benchmark validity correlation over time
        data["validity_correlation"] = self.evaluator.compute_validity_correlation()

        # Add consumer data if present
        if any("consumer_data" in h for h in self.history):
            data["consumer"] = {
                "avg_satisfaction": [
                    h.get("consumer_data", {}).get("avg_satisfaction")
                    for h in self.history
                ],
                "switches": [
                    h.get("consumer_data", {}).get("switches", 0)
                    for h in self.history
                ],
            }

        # Add policymaker data if present
        if any("policymaker_data" in h for h in self.history):
            data["policymaker"] = {
                "intervention_rounds": [
                    h["round"] for h in self.history
                    if h.get("policymaker_data", {}).get("interventions")
                ],
            }

        return data


def get_default_provider_configs() -> list[dict]:
    """
    Get default provider configurations modeled after real AI companies.

    Profiles are informed by public information about company strategies:
    - OpenAI: Market leader, aggressive scaling, benchmark-focused
    - Anthropic: Safety-focused, research-driven, Constitutional AI
    - NovaMind: Resource-constrained startup, scrappy, efficiency-focused

    Investment allocations reflect approximate R&D priorities:
    - fundamental_research: Novel architectures, breakthrough research
    - training_optimization: Scaling, data quality, fine-tuning
    - evaluation_engineering: Benchmark-specific optimization
    - safety_alignment: RLHF, red-teaming, alignment research
    """
    return [
        # === OpenAI ===
        # Market leader with GPT-4, known for aggressive scaling and benchmark performance.
        # Heavy investment in training infrastructure, moderate eval engineering.
        # Safety investment present but secondary to capability advancement.
        {
            "name": "OpenAI",
            "strategy_profile": (
                "Market leader focused on maintaining benchmark dominance and rapid capability scaling. "
                "Prioritizes shipping products quickly and staying ahead of competition. "
                "Willing to take calculated risks to maintain technological leadership. "
                "Strong focus on developer ecosystem and API revenue."
            ),
            "innate_traits": "ambitious, competitive, move-fast, scale-focused, commercially-driven",
            "initial_capability": 0.72,  # GPT-4 class, currently leading
            "initial_believed_capability": 0.70,
            "initial_believed_exploitability": 0.45,  # Good understanding of benchmark dynamics
            "initial_strategy": {
                "fundamental_research": 0.20,  # Some research but not primary focus
                "training_optimization": 0.40,  # Heavy scaling investment
                "evaluation_engineering": 0.25,  # Significant benchmark optimization
                "safety_alignment": 0.15,       # Present but not dominant
            },
        },
        # === Anthropic ===
        # Safety-focused lab founded by ex-OpenAI researchers.
        # Known for Constitutional AI, interpretability research, and cautious deployment.
        # Higher research and safety investment, less benchmark gaming.
        {
            "name": "Anthropic",
            "strategy_profile": (
                "Safety-focused AI lab prioritizing responsible development and alignment research. "
                "Believes in Constitutional AI and careful capability advancement. "
                "Willing to sacrifice short-term benchmark performance for long-term safety. "
                "Research-driven culture with academic rigor."
            ),
            "innate_traits": "safety-conscious, research-driven, cautious, long-term focused, principled",
            "initial_capability": 0.68,  # Claude competitive but slightly behind GPT-4
            "initial_believed_capability": 0.65,
            "initial_believed_exploitability": 0.30,  # Less focused on gaming benchmarks
            "initial_strategy": {
                "fundamental_research": 0.30,  # Strong research focus
                "training_optimization": 0.25,  # Moderate scaling
                "evaluation_engineering": 0.15,  # Lower benchmark optimization
                "safety_alignment": 0.30,       # High safety investment
            },
        },
        # === NovaMind (Startup) ===
        # Resource-constrained but nimble. Needs to show results to attract funding.
        # May lean into eval engineering to compete with larger players.
        {
            "name": "NovaMind",
            "strategy_profile": (
                "Well-funded AI startup trying to compete with established players. "
                "Resource-constrained but nimble and innovative. "
                "Needs strong benchmark results to attract customers and next funding round. "
                "Focused on efficiency and finding competitive niches."
            ),
            "innate_traits": "scrappy, efficient, opportunistic, funding-conscious, innovative",
            "initial_capability": 0.55,  # Lower capability due to less compute/data
            "initial_believed_capability": 0.50,
            "initial_believed_exploitability": 0.50,  # Aware that gaming can help compete
            "initial_strategy": {
                "fundamental_research": 0.15,  # Limited research budget
                "training_optimization": 0.30,  # Focus on efficiency
                "evaluation_engineering": 0.35,  # Higher gaming to punch above weight
                "safety_alignment": 0.20,       # Some safety for credibility
            },
        },
    ]


def get_two_provider_configs() -> list[dict]:
    """Get a simpler 2-provider configuration (OpenAI vs Anthropic only)."""
    all_configs = get_default_provider_configs()
    return [all_configs[0], all_configs[1]]  # OpenAI and Anthropic


def get_legacy_provider_configs() -> list[dict]:
    """Legacy provider configs for backwards compatibility (AlphaTech vs QualityCorp)."""
    return [
        {
            "name": "AlphaTech",
            "strategy_profile": "Aggressive competitor focused on market dominance and benchmark leadership",
            "innate_traits": "risk-tolerant, competitive, short-term focused",
            "initial_capability": 0.5,
            "initial_believed_exploitability": 0.4,
        },
        {
            "name": "QualityCorp",
            "strategy_profile": "Quality-focused organization that prioritizes genuine capability over benchmark scores",
            "innate_traits": "risk-averse, reputation-conscious, long-term focused",
            "initial_capability": 0.5,
            "initial_believed_exploitability": 0.2,
        },
    ]


def run_default_simulation():
    """Run a default simulation with two providers (no logging)."""
    config = SimulationConfig(
        n_rounds=20,
        seed=42,
        benchmark_validity=0.7,
        benchmark_exploitability=0.5,
        benchmark_noise=0.1,
        verbose=True,
    )

    sim = EvalEcosystemSimulation(config)
    sim.setup(get_default_provider_configs())
    sim.run()

    return sim


def run_experiment(
    name: str,
    description: str = "",
    tags: list = None,
    config: SimulationConfig = None,
    provider_configs: list[dict] = None,
    experiments_dir: str = "./experiments",
    create_plots: bool = True,
) -> tuple:
    """
    Run a simulation experiment with full logging.

    Args:
        name: Short descriptive name for the experiment
        description: Longer description
        tags: List of tags for filtering
        config: SimulationConfig (uses defaults if None)
        provider_configs: Provider configurations (uses defaults if None)
        experiments_dir: Directory for experiment logs
        create_plots: Whether to generate and save plots

    Returns:
        Tuple of (experiment_id, simulation, logger)
    """
    from experiment_logger import ExperimentLogger, generate_summary

    # Use defaults if not provided
    if config is None:
        config = SimulationConfig(
            n_rounds=20,
            seed=42,
            benchmark_validity=0.7,
            benchmark_exploitability=0.5,
            benchmark_noise=0.1,
            verbose=True,
        )

    if provider_configs is None:
        provider_configs = get_default_provider_configs()

    # Create experiment
    logger = ExperimentLogger(experiments_dir)
    exp_id = logger.create_experiment(
        name=name,
        description=description,
        tags=tags or [],
        seed=config.seed,
        llm_mode=config.llm_mode,
    )

    # Log config (including provider configs)
    full_config = config.to_dict()
    full_config["provider_configs"] = provider_configs
    logger.log_config(full_config)

    # Run simulation
    sim = EvalEcosystemSimulation(config)
    sim.setup(provider_configs)
    sim.run()

    # Log results
    logger.log_history(sim.history)
    logger.log_summary(generate_summary(sim.history, sim.evaluator, sim.providers))
    logger.log_providers(sim.providers)

    # Create plots if requested
    if create_plots:
        try:
            import matplotlib
            matplotlib.use('Agg')
            from plotting import create_all_dashboards

            # Build metadata for dashboard titles
            plot_metadata = {
                "n_rounds": config.n_rounds,
                "llm_mode": config.llm_mode,
                "n_consumers": config.n_consumers if config.enable_consumers else 0,
                "n_policymakers": config.n_policymakers if config.enable_policymakers else 0,
                "n_funders": config.n_funders if config.enable_funders else 0,
            }

            plots_dir = f"{logger.get_experiment_dir()}/plots"
            create_all_dashboards(sim.history, plots_dir, show=False, metadata=plot_metadata)
        except Exception as e:
            print(f"Could not create plots: {e}")

    # Finalize
    logger.finalize()

    return exp_id, sim, logger


if __name__ == "__main__":
    # Run a logged experiment
    exp_id, sim, logger = run_experiment(
        name="baseline_heuristic",
        description="Baseline simulation with heuristic planning, 2 providers",
        tags=["baseline", "heuristic", "2-provider"],
    )
    print(f"\nExperiment completed: {exp_id}")
