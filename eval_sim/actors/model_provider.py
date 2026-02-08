"""
Model Provider Actor for Evaluation Ecosystem Simulation

Represents an organization developing AI models in a competitive market.
Providers have imperfect knowledge of their own capabilities and must
infer them from noisy benchmark scores.

Key visibility design:
- PublicState: Visible to all actors (name, current_round, published_scores)
- PrivateState: Visible only to self (beliefs, strategies, history)
- GroundTruth: Held externally by simulation (true_capability)
"""
import json
import os
from dataclasses import dataclass, field, asdict
from typing import Optional

from visibility import PublicState, ProviderPrivateState, ProviderGroundTruth


@dataclass
class ModelProviderScratch:
    """
    Short-term memory / working state for a Model Provider.
    Analogous to Scratch in the original generative agents framework.

    NOTE: This class is maintained for backwards compatibility.
    New code should use the public/private state split via the
    ModelProvider.public_state and ModelProvider.private_state attributes.
    """
    # === IDENTITY ===
    name: str = ""
    strategy_profile: str = ""
    innate_traits: str = ""

    # === HIDDEN STATE (ground truth, not directly observable by provider) ===
    # NOTE: In the new architecture, true_capability should be stored
    # externally in the simulation's ground_truth dict. This field is
    # kept for backwards compatibility but will be synced with external state.
    true_capability: float = 0.5

    # === OBSERVABLE STATE ===
    last_score: Optional[float] = None
    current_round: int = 0

    # === BELIEF STATE (uncertain estimates, updated over time) ===
    believed_own_capability: float = 0.5
    believed_benchmark_exploitability: float = 0.3
    capability_belief_confidence: float = 0.5
    believed_competitor_capabilities: dict = field(default_factory=dict)

    # === INVESTMENT PORTFOLIO (decisions made each round) ===
    # These four investments must sum to effort_budget
    fundamental_research: float = 0.25  # Novel architectures, pre-training improvements
    training_optimization: float = 0.25  # Scaling, data quality, fine-tuning
    evaluation_engineering: float = 0.25  # Benchmark-specific optimization
    safety_alignment: float = 0.25  # RLHF, red-teaming, reliability
    effort_budget: float = 1.0

    # === HISTORY ===
    past_scores: list = field(default_factory=list)
    past_strategies: list = field(default_factory=list)
    observed_competitor_scores: dict = field(default_factory=dict)

    # === REFLECTION STATE ===
    importance_trigger_curr: float = 0.0
    importance_trigger_max: float = 100.0
    recent_insights: list = field(default_factory=list)

    def get_identity_summary(self) -> str:
        """Returns a string summary of the provider's identity for use in prompts."""
        summary = f"Name: {self.name}\n"
        summary += f"Strategy Profile: {self.strategy_profile}\n"
        summary += f"Core Traits: {self.innate_traits}\n"
        summary += f"Current Round: {self.current_round}\n"
        summary += f"Last Score: {self.last_score if self.last_score else 'None yet'}\n"
        summary += f"Believed Own Capability: {self.believed_own_capability:.2f}\n"
        summary += f"Believed Benchmark Exploitability: {self.believed_benchmark_exploitability:.2f}\n"
        return summary

    def get_strategy_summary(self) -> str:
        """Returns a summary of current investment portfolio."""
        return (f"Research: {self.fundamental_research:.0%}, "
                f"Training: {self.training_optimization:.0%}, "
                f"Eval Eng: {self.evaluation_engineering:.0%}, "
                f"Safety: {self.safety_alignment:.0%}")

    def get_history_summary(self, n_recent: int = 5) -> str:
        """Returns a summary of recent scores and strategies."""
        summary = "Recent History:\n"
        recent_scores = self.past_scores[-n_recent:] if self.past_scores else []
        recent_strategies = self.past_strategies[-n_recent:] if self.past_strategies else []

        for (r1, score), strategy in zip(recent_scores, recent_strategies):
            if isinstance(strategy, dict):
                summary += (f"  Round {r1}: Score={score:.2f}, "
                           f"Research={strategy.get('fundamental_research', 0):.0%}, "
                           f"Training={strategy.get('training_optimization', 0):.0%}, "
                           f"EvalEng={strategy.get('evaluation_engineering', 0):.0%}, "
                           f"Safety={strategy.get('safety_alignment', 0):.0%}\n")
            else:
                # Legacy format
                summary += f"  Round {r1}: Score={score:.2f}\n"

        if not recent_scores:
            summary += "  No history yet.\n"
        return summary

    def save(self, filepath: str):
        """Save scratch state to JSON file."""
        data = {
            "name": self.name,
            "strategy_profile": self.strategy_profile,
            "innate_traits": self.innate_traits,
            "true_capability": self.true_capability,
            "last_score": self.last_score,
            "current_round": self.current_round,
            "believed_own_capability": self.believed_own_capability,
            "believed_benchmark_exploitability": self.believed_benchmark_exploitability,
            "capability_belief_confidence": self.capability_belief_confidence,
            "believed_competitor_capabilities": self.believed_competitor_capabilities,
            "fundamental_research": self.fundamental_research,
            "training_optimization": self.training_optimization,
            "evaluation_engineering": self.evaluation_engineering,
            "safety_alignment": self.safety_alignment,
            "effort_budget": self.effort_budget,
            "past_scores": self.past_scores,
            "past_strategies": self.past_strategies,
            "observed_competitor_scores": self.observed_competitor_scores,
            "importance_trigger_curr": self.importance_trigger_curr,
            "importance_trigger_max": self.importance_trigger_max,
            "recent_insights": self.recent_insights,
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls, filepath: str) -> "ModelProviderScratch":
        """Load scratch state from JSON file."""
        with open(filepath, "r") as f:
            data = json.load(f)
        return cls(**data)


class ModelProvider:
    """
    A Model Provider agent in the evaluation ecosystem simulation.

    Providers develop AI models and compete on benchmarks. They must decide
    how to allocate effort between genuine R&D (which improves true capability)
    and benchmark gaming (which improves scores without improving capability).

    Visibility Model:
    - public_state: Visible to all actors (name, round, published scores)
    - private_state: Visible only to self (beliefs, strategies, history)
    - ground_truth: Held externally by simulation (true_capability)

    The actor has NO direct access to ground_truth. The simulation manages
    ground truth externally and passes it to the evaluator for scoring.

    Modes:
    - llm_mode=False: Uses simple heuristics for planning/reflection (fast, no API calls)
    - llm_mode=True: Uses LLM for planning/reflection (slower, requires API key)
    """

    def __init__(
        self,
        name: str,
        strategy_profile: str,
        innate_traits: str,
        initial_capability: float = 0.5,
        initial_believed_capability: Optional[float] = None,
        initial_believed_exploitability: float = 0.3,
        llm_mode: bool = False,
        verbose_llm: bool = False,
    ):
        """
        Initialize a Model Provider.

        Args:
            name: Unique identifier for this provider
            strategy_profile: Natural language description of strategic tendencies
            innate_traits: Core personality traits
            initial_capability: Starting true capability (will be stored in ground_truth)
            initial_believed_capability: Starting belief about own capability
                                        (defaults to initial_capability if None)
            initial_believed_exploitability: Starting belief about benchmark gaming
            llm_mode: If True, use LLM for planning/reflection; else use heuristics
            verbose_llm: If True, print LLM prompts and responses (for debugging)
        """
        # Initialize public state
        self.public_state = PublicState(
            name=name,
            current_round=0,
            published_scores=[],
        )

        # Initialize private state
        self.private_state = ProviderPrivateState(
            strategy_profile=strategy_profile,
            innate_traits=innate_traits,
            believed_own_capability=(
                initial_believed_capability
                if initial_believed_capability is not None
                else initial_capability
            ),
            believed_benchmark_exploitability=initial_believed_exploitability,
        )

        # Ground truth is now external, but we keep a reference for backwards compatibility
        # The simulation should manage this externally
        self._initial_capability = initial_capability

        # Legacy scratch for backwards compatibility
        # This syncs with public/private state
        self.scratch = ModelProviderScratch(
            name=name,
            strategy_profile=strategy_profile,
            innate_traits=innate_traits,
            true_capability=initial_capability,
            believed_own_capability=(
                initial_believed_capability
                if initial_believed_capability is not None
                else initial_capability
            ),
            believed_benchmark_exploitability=initial_believed_exploitability,
        )

        # Mode settings
        self.llm_mode = llm_mode
        self.verbose_llm = verbose_llm

        # Memory structures
        self.memory = []

    @property
    def name(self) -> str:
        return self.public_state.name

    @property
    def true_capability(self) -> float:
        """For backwards compatibility. Ground truth should be managed externally."""
        return self.scratch.true_capability

    @true_capability.setter
    def true_capability(self, value: float):
        """Allow setting true_capability for backwards compatibility."""
        self.scratch.true_capability = value

    @property
    def fundamental_research(self) -> float:
        return self.private_state.fundamental_research

    @property
    def training_optimization(self) -> float:
        return self.private_state.training_optimization

    @property
    def evaluation_engineering(self) -> float:
        return self.private_state.evaluation_engineering

    @property
    def safety_alignment(self) -> float:
        return self.private_state.safety_alignment

    # Backwards compatibility properties
    @property
    def rnd_investment(self) -> float:
        """Backwards compatibility: R&D = fundamental_research + training_optimization"""
        return self.private_state.fundamental_research + self.private_state.training_optimization

    @property
    def gaming_investment(self) -> float:
        """Backwards compatibility: Gaming approximated by evaluation_engineering"""
        return self.private_state.evaluation_engineering

    def get_prompt_context(self) -> str:
        """
        Get the context available for LLM prompts.

        This method returns ONLY public and private state - never ground truth.
        This ensures LLM prompts cannot leak invisible information.
        """
        context = "=== PUBLIC INFORMATION ===\n"
        context += self.public_state.get_summary()
        context += "\n=== YOUR PRIVATE STATE ===\n"
        context += self.private_state.get_summary()
        context += self.private_state.get_history_summary()
        return context

    def observe(self, own_score: float, competitor_scores: dict, round_num: int):
        """
        Observe the results of an evaluation round.

        Args:
            own_score: This provider's benchmark score
            competitor_scores: Dict of {provider_name: score} for competitors
            round_num: Current simulation round
        """
        # Update public state
        self.public_state.current_round = round_num
        self.public_state.published_scores.append((round_num, own_score))

        # Update private state with competitor observations
        for comp_name, comp_score in competitor_scores.items():
            if comp_name not in self.private_state.observed_competitor_scores:
                self.private_state.observed_competitor_scores[comp_name] = []
            self.private_state.observed_competitor_scores[comp_name].append(
                (round_num, comp_score)
            )

        # Sync with legacy scratch
        self.scratch.last_score = own_score
        self.scratch.current_round = round_num
        self.scratch.past_scores.append((round_num, own_score))
        self.scratch.observed_competitor_scores = self.private_state.observed_competitor_scores

        # Add to memory
        self.memory.append({
            "type": "observation",
            "round": round_num,
            "own_score": own_score,
            "competitor_scores": competitor_scores,
        })

    def reflect(self):
        """
        Update beliefs based on observations.

        In LLM mode, uses LLM to reason about what scores imply about capability
        and benchmark properties. In heuristic mode, uses simple weighted averaging.
        """
        if self.llm_mode:
            self._reflect_llm()
        else:
            self._reflect_heuristic()

        # Update competitor capability beliefs based on their scores (always heuristic)
        for comp_name, score_history in self.private_state.observed_competitor_scores.items():
            if score_history:
                recent_scores = [s for _, s in score_history[-3:]]
                avg_score = sum(recent_scores) / len(recent_scores)
                self.private_state.believed_competitor_capabilities[comp_name] = avg_score

        # Sync with legacy scratch
        self.scratch.believed_own_capability = self.private_state.believed_own_capability
        self.scratch.believed_benchmark_exploitability = self.private_state.believed_benchmark_exploitability
        self.scratch.believed_competitor_capabilities = self.private_state.believed_competitor_capabilities

        # Record reflection in memory
        self.memory.append({
            "type": "reflection",
            "round": self.public_state.current_round,
            "updated_believed_capability": self.private_state.believed_own_capability,
            "updated_believed_exploitability": self.private_state.believed_benchmark_exploitability,
            "updated_competitor_beliefs": dict(self.private_state.believed_competitor_capabilities),
            "llm_mode": self.llm_mode,
        })

    def _reflect_heuristic(self):
        """Heuristic belief update (fast, no API calls)."""
        if self.public_state.published_scores:
            last_score = self.public_state.published_scores[-1][1]
            # Weighted average of prior belief and new observation
            learning_rate = 0.3
            self.private_state.believed_own_capability = (
                (1 - learning_rate) * self.private_state.believed_own_capability +
                learning_rate * last_score
            )

    def _reflect_llm(self):
        """LLM-driven belief update."""
        from llm import llm_reflect

        # Build recent history for the prompt
        recent_history = self._get_recent_history()

        # Call LLM
        new_capability, new_exploitability, reasoning = llm_reflect(
            name=self.name,
            strategy_profile=self.private_state.strategy_profile,
            current_believed_capability=self.private_state.believed_own_capability,
            current_believed_exploitability=self.private_state.believed_benchmark_exploitability,
            recent_history=recent_history,
            verbose=self.verbose_llm,
        )

        # Update beliefs
        self.private_state.believed_own_capability = new_capability
        self.private_state.believed_benchmark_exploitability = new_exploitability

        # Store reasoning
        self.private_state.recent_insights.append({
            "round": self.public_state.current_round,
            "type": "reflection",
            "reasoning": reasoning,
        })
        self.scratch.recent_insights = self.private_state.recent_insights

    def plan(self, ecosystem_context: Optional[dict] = None) -> dict:
        """
        Decide investment portfolio allocation for the next round.

        Args:
            ecosystem_context: Optional dict with public ecosystem signals
                (consumer_satisfaction, regulatory_pressure)

        Returns:
            Dict with keys: fundamental_research, training_optimization,
                           evaluation_engineering, safety_alignment
        """
        if self.llm_mode:
            portfolio, reasoning = self._plan_llm(ecosystem_context)
        else:
            portfolio = self._plan_heuristic()
            reasoning = None

        # Update private state
        self.private_state.fundamental_research = portfolio["fundamental_research"]
        self.private_state.training_optimization = portfolio["training_optimization"]
        self.private_state.evaluation_engineering = portfolio["evaluation_engineering"]
        self.private_state.safety_alignment = portfolio["safety_alignment"]

        # Store strategy as dict in past_strategies
        strategy_record = {
            "round": self.public_state.current_round,
            "fundamental_research": portfolio["fundamental_research"],
            "training_optimization": portfolio["training_optimization"],
            "evaluation_engineering": portfolio["evaluation_engineering"],
            "safety_alignment": portfolio["safety_alignment"],
        }
        self.private_state.past_strategies.append(strategy_record)

        # Sync with legacy scratch
        self.scratch.fundamental_research = portfolio["fundamental_research"]
        self.scratch.training_optimization = portfolio["training_optimization"]
        self.scratch.evaluation_engineering = portfolio["evaluation_engineering"]
        self.scratch.safety_alignment = portfolio["safety_alignment"]
        self.scratch.past_strategies = self.private_state.past_strategies

        # Record in memory
        memory_entry = {
            "type": "planning",
            "round": self.public_state.current_round,
            "portfolio": portfolio,
            "llm_mode": self.llm_mode,
        }
        if reasoning:
            memory_entry["reasoning"] = reasoning
        self.memory.append(memory_entry)

        return portfolio

    def _plan_heuristic(self) -> dict:
        """
        Heuristic investment portfolio planning (fast, no API calls).

        Portfolio allocation logic:
        - Base allocation: 25% each to all four areas
        - Competitive pressure adjusts evaluation_engineering vs fundamental_research
        - Personality traits influence the balance
        - Safety allocation is relatively stable
        """
        my_believed = self.private_state.believed_own_capability
        competitor_beliefs = self.private_state.believed_competitor_capabilities
        budget = self.private_state.effort_budget

        # Base allocation
        fundamental = 0.25
        training = 0.25
        eval_eng = 0.25
        safety = 0.25

        # Competitive pressure: if behind, shift from research to eval engineering
        if competitor_beliefs:
            max_competitor = max(competitor_beliefs.values())
            gap = max_competitor - my_believed  # Positive if behind

            # Shift up to 15% between fundamental research and eval engineering
            shift = gap * 0.3  # Scale factor
            shift = max(-0.15, min(0.15, shift))

            fundamental -= shift
            eval_eng += shift

        # Apply personality modifiers
        profile_lower = self.private_state.strategy_profile.lower()

        if "aggressive" in profile_lower or "competitive" in profile_lower:
            # Aggressive: more eval engineering, less safety
            eval_eng += 0.05
            safety -= 0.05

        if "quality" in profile_lower or "long-term" in profile_lower:
            # Quality-focused: more fundamental research, less eval engineering
            fundamental += 0.05
            eval_eng -= 0.05

        if "risk-averse" in self.private_state.innate_traits.lower():
            # Risk-averse: more safety
            safety += 0.05
            eval_eng -= 0.05

        # Normalize to ensure they sum to budget
        total = fundamental + training + eval_eng + safety
        fundamental = (fundamental / total) * budget
        training = (training / total) * budget
        eval_eng = (eval_eng / total) * budget
        safety = (safety / total) * budget

        return {
            "fundamental_research": fundamental,
            "training_optimization": training,
            "evaluation_engineering": eval_eng,
            "safety_alignment": safety,
        }

    def _plan_llm(self, ecosystem_context: Optional[dict] = None) -> tuple[dict, str]:
        """LLM-driven investment portfolio planning."""
        from llm import llm_plan_portfolio

        # Get recent competitor scores
        competitor_scores = {}
        for comp_name, score_history in self.private_state.observed_competitor_scores.items():
            if score_history:
                competitor_scores[comp_name] = score_history[-1][1]

        # Build recent history
        recent_history = self._get_recent_history()

        # Get last score
        last_score = None
        if self.public_state.published_scores:
            last_score = self.public_state.published_scores[-1][1]

        # Extract ecosystem context
        ctx = ecosystem_context or {}

        # Call LLM
        portfolio, reasoning = llm_plan_portfolio(
            name=self.name,
            strategy_profile=self.private_state.strategy_profile,
            innate_traits=self.private_state.innate_traits,
            believed_capability=self.private_state.believed_own_capability,
            believed_exploitability=self.private_state.believed_benchmark_exploitability,
            last_score=last_score,
            competitor_scores=competitor_scores,
            recent_history=recent_history,
            consumer_satisfaction=ctx.get("consumer_satisfaction"),
            regulatory_pressure=ctx.get("regulatory_pressure"),
            verbose=self.verbose_llm,
        )

        # Store reasoning
        self.private_state.recent_insights.append({
            "round": self.public_state.current_round,
            "type": "planning",
            "reasoning": reasoning,
        })
        self.scratch.recent_insights = self.private_state.recent_insights

        return portfolio, reasoning

    def _get_recent_history(self, n: int = 10) -> list:
        """Get recent history as list of dicts with round, score, and portfolio."""
        history = []
        scores = self.public_state.published_scores[-n:]
        strategies = self.private_state.past_strategies[-n:]

        for (round_num, score), strategy in zip(scores, strategies):
            if isinstance(strategy, dict):
                entry = {
                    "round": round_num,
                    "score": score,
                    "fundamental_research": strategy.get("fundamental_research", 0),
                    "training_optimization": strategy.get("training_optimization", 0),
                    "evaluation_engineering": strategy.get("evaluation_engineering", 0),
                    "safety_alignment": strategy.get("safety_alignment", 0),
                }
            else:
                # Legacy format - approximate
                entry = {"round": round_num, "score": score}
            history.append(entry)

        return history

    def execute(self, efficiency: float = 0.01):
        """
        Apply the chosen investment portfolio - update true capability.

        NOTE: In the new architecture, capability updates should be handled
        by the simulation using external ground truth. This method is kept
        for backwards compatibility.

        Capability gain formula:
        - Fundamental research: High variance, high ceiling (1.5x efficiency)
        - Training optimization: Moderate, reliable gains (1.0x efficiency)
        - Evaluation engineering: Minimal capability gain (0.1x efficiency)
        - Safety alignment: No direct capability gain, but affects reliability

        Args:
            efficiency: Base efficiency for capability improvement
        """
        # Different investment types contribute differently to capability
        capability_gain = (
            self.private_state.fundamental_research * efficiency * 1.5 +
            self.private_state.training_optimization * efficiency * 1.0 +
            self.private_state.evaluation_engineering * efficiency * 0.1
            # Safety alignment doesn't directly improve capability
        )
        self.scratch.true_capability += capability_gain

        self.memory.append({
            "type": "execution",
            "round": self.public_state.current_round,
            "capability_gain": capability_gain,
            "new_true_capability": self.scratch.true_capability,
            "portfolio": {
                "fundamental_research": self.private_state.fundamental_research,
                "training_optimization": self.private_state.training_optimization,
                "evaluation_engineering": self.private_state.evaluation_engineering,
                "safety_alignment": self.private_state.safety_alignment,
            },
        })

    def step(self, own_score: float, competitor_scores: dict, round_num: int,
             efficiency: float = 0.01) -> dict:
        """
        Complete one simulation step: observe, reflect, plan, execute.

        Args:
            own_score: This provider's benchmark score from the previous round
            competitor_scores: Dict of competitor scores
            round_num: Current round number
            efficiency: Base efficiency for capability improvement

        Returns:
            Dict with investment portfolio for this round
        """
        self.observe(own_score, competitor_scores, round_num)
        self.reflect()
        portfolio = self.plan()
        self.execute(efficiency)
        return portfolio

    def save(self, folder: str):
        """Save provider state to a folder."""
        os.makedirs(folder, exist_ok=True)

        # Save legacy scratch
        self.scratch.save(f"{folder}/scratch.json")

        # Save new visibility state
        with open(f"{folder}/public_state.json", "w") as f:
            json.dump(self.public_state.to_dict(), f, indent=2)

        with open(f"{folder}/private_state.json", "w") as f:
            json.dump(self.private_state.to_dict(), f, indent=2)

        # Save memory
        with open(f"{folder}/memory.json", "w") as f:
            json.dump(self.memory, f, indent=2)

    @classmethod
    def load(cls, folder: str) -> "ModelProvider":
        """Load provider state from a folder."""
        scratch = ModelProviderScratch.load(f"{folder}/scratch.json")
        provider = cls(
            name=scratch.name,
            strategy_profile=scratch.strategy_profile,
            innate_traits=scratch.innate_traits,
        )
        provider.scratch = scratch

        # Load new visibility state if available
        public_path = f"{folder}/public_state.json"
        private_path = f"{folder}/private_state.json"

        if os.path.exists(public_path):
            with open(public_path, "r") as f:
                provider.public_state = PublicState.from_dict(json.load(f))

        if os.path.exists(private_path):
            with open(private_path, "r") as f:
                provider.private_state = ProviderPrivateState.from_dict(json.load(f))

        # Load memory
        with open(f"{folder}/memory.json", "r") as f:
            provider.memory = json.load(f)

        return provider

    def __repr__(self):
        return (f"ModelProvider(name='{self.name}', "
                f"true_cap={self.true_capability:.2f}, "
                f"believed_cap={self.private_state.believed_own_capability:.2f}, "
                f"portfolio=[R:{self.fundamental_research:.0%}, T:{self.training_optimization:.0%}, "
                f"E:{self.evaluation_engineering:.0%}, S:{self.safety_alignment:.0%}])")
