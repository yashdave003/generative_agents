"""
Funder Actor for Evaluation Ecosystem Simulation

Represents capital allocators (VCs, Government/AISI, Foundations) who influence
provider development through funding decisions.

Key dynamics:
- Funders observe leaderboard, consumer satisfaction, and regulatory interventions
- They infer provider quality from public signals (cannot see strategies directly)
- Funding affects providers via efficiency multiplier on capability gains
- Different funder types have different allocation strategies

Funder Types:
- VC: ROI maximization, back top performers, high concentration
- Government/AISI: Safety & stability, spread funding, favor consistency
- Foundation: Mission alignment, reward capability growth

Visibility:
- PUBLIC: name, active investments (provider names only)
- PRIVATE: funder_type, beliefs, allocation history, mission
- INVISIBLE: true_roi, actual funding effectiveness
"""
import json
import os
from dataclasses import dataclass, field
from typing import Optional

from visibility import PublicState, FunderPrivateState, FunderGroundTruth


class Funder:
    """
    A Funder agent in the evaluation ecosystem simulation.

    Funders are capital allocators who:
    1. Observe ecosystem state (leaderboard, consumer satisfaction, regulatory interventions)
    2. Infer provider quality from public signals
    3. Allocate funding to providers based on their type and strategy
    4. Funding affects provider capability gains via efficiency multiplier

    This creates capital-side pressure: good performance and low gaming attracts funding,
    which creates advantages in capability development.

    Visibility Model:
    - public_state: Visible to all (name, funded providers)
    - private_state: Visible only to self (type, beliefs, allocations)
    - ground_truth: Held by simulation (true ROI, effectiveness)
    """

    def __init__(
        self,
        name: str,
        funder_type: str = "vc",
        total_capital: float = 1000000.0,
        risk_tolerance: float = 0.5,
        mission_statement: str = "",
        llm_mode: bool = False,
        max_round_deployment: float = 0.10,
        funding_cooldown: int = 2,
    ):
        """
        Initialize a Funder.

        Args:
            name: Unique identifier for this funder
            funder_type: Type of funder ("vc", "gov", "foundation")
            total_capital: Total capital available for funding
            risk_tolerance: How much risk is acceptable (0-1)
            mission_statement: Mission-driven objective (for foundation type)
            llm_mode: If True, use LLM for decision-making
            max_round_deployment: Fraction of total_capital deployable per round (default 10%)
            funding_cooldown: Rounds between new allocation decisions (default 2)
        """
        # Initialize public state
        self.public_state = PublicState(
            name=name,
            current_round=0,
            published_scores=[],  # Reused to track public funding announcements
        )

        # Initialize private state
        self.private_state = FunderPrivateState(
            funder_type=funder_type,
            mission_statement=mission_statement,
            total_capital=total_capital,
            deployed_capital=0.0,
            believed_provider_quality={},
            believed_provider_gaming={},
            active_funding={},
            funding_history=[],
            roi_history=[],
        )

        # Funder-specific parameters
        self.risk_tolerance = risk_tolerance
        self.llm_mode = llm_mode
        self.max_round_deployment = max_round_deployment
        self.funding_cooldown = funding_cooldown

        # Memory
        self.memory = []

        # Tracking for inference
        self._last_leaderboard: list = []
        self._last_consumer_data: dict = {}
        self._last_policymaker_data: dict = {}
        self._previous_scores: dict = {}  # For computing score growth

        # Momentum tracking
        self._score_history: list[dict] = []  # [{provider: score}, ...] last N rounds
        self._previous_market_shares: dict = {}  # {provider: share} from prior round

        # Cooldown tracking
        self._last_funding_round: int = -2  # Ensures funding happens on round 0

    @property
    def name(self) -> str:
        return self.public_state.name

    @property
    def funder_type(self) -> str:
        return self.private_state.funder_type

    def observe(
        self,
        leaderboard: list,
        consumer_data: dict,
        policymaker_data: dict,
        round_num: int,
        media_coverage: Optional[dict] = None,
        other_funder_allocations: Optional[dict] = None,
    ):
        """
        Observe the current ecosystem state.

        Funders can only see public signals:
        - Leaderboard scores (performance)
        - Consumer satisfaction (true quality proxy)
        - Regulatory interventions (compliance/safety risk)
        - Media coverage (sentiment, risk signals)
        - Other funders' allocations (for portfolio diversification)

        Args:
            leaderboard: List of (provider_name, score) tuples
            consumer_data: Dict with avg_satisfaction, provider_satisfaction, etc.
            policymaker_data: Dict with interventions, active_regulations
            round_num: Current simulation round
            media_coverage: Optional media coverage dict
            other_funder_allocations: Dict of {funder_name: {provider: amount}}
        """
        self.public_state.current_round = round_num

        # Store for inference
        self._last_leaderboard = leaderboard
        self._last_consumer_data = consumer_data
        self._last_policymaker_data = policymaker_data
        self._other_funder_allocations = other_funder_allocations or {}

        # Update beliefs about provider quality using public signals
        for provider_name, score in leaderboard:
            # Get consumer satisfaction (if available)
            satisfaction = self._get_provider_satisfaction(provider_name, consumer_data)

            # Infer quality: blend of score and satisfaction
            # Satisfaction is a better proxy for true quality
            if satisfaction is not None:
                inferred_quality = 0.4 * score + 0.6 * satisfaction
            else:
                inferred_quality = score

            # Update belief with learning rate
            if provider_name not in self.private_state.believed_provider_quality:
                self.private_state.believed_provider_quality[provider_name] = inferred_quality
            else:
                learning_rate = 0.3
                old_belief = self.private_state.believed_provider_quality[provider_name]
                self.private_state.believed_provider_quality[provider_name] = (
                    (1 - learning_rate) * old_belief + learning_rate * inferred_quality
                )

            # Infer gaming level from satisfaction gap
            # High score + low satisfaction = likely gaming
            if satisfaction is not None:
                satisfaction_gap = score - satisfaction
                # Positive gap suggests gaming
                gaming_estimate = max(0, min(1, satisfaction_gap * 2))
            else:
                gaming_estimate = 0.3  # Default assumption

            if provider_name not in self.private_state.believed_provider_gaming:
                self.private_state.believed_provider_gaming[provider_name] = gaming_estimate
            else:
                old_gaming = self.private_state.believed_provider_gaming[provider_name]
                self.private_state.believed_provider_gaming[provider_name] = (
                    0.7 * old_gaming + 0.3 * gaming_estimate
                )

        # Media coverage influences funder sentiment
        if media_coverage:
            sentiment = media_coverage.get("sentiment", 0.0)
            provider_attention = media_coverage.get("provider_attention", {})
            risk_signals = media_coverage.get("risk_signals", [])

            # Negative coverage about a provider increases believed_gaming
            for provider_name in [name for name, _ in leaderboard]:
                attention = provider_attention.get(provider_name, 0)
                if attention > 0.3 and risk_signals:
                    # High media attention + risk signals → increase gaming estimate
                    gaming_bump = attention * 0.1
                    if provider_name in self.private_state.believed_provider_gaming:
                        self.private_state.believed_provider_gaming[provider_name] = min(
                            1.0,
                            self.private_state.believed_provider_gaming[provider_name] + gaming_bump,
                        )

        # Store previous scores for growth calculation
        self._previous_scores = {name: score for name, score in leaderboard}

        # Track score history for momentum (keep last 4 snapshots to compute 3-round deltas)
        current_scores = {name: score for name, score in leaderboard}
        self._score_history.append(current_scores)
        if len(self._score_history) > 4:
            self._score_history = self._score_history[-4:]

        # Track market share momentum
        market_shares = consumer_data.get("market_shares", {})
        self._current_market_momentum = {}
        for provider_name in [name for name, _ in leaderboard]:
            curr_share = market_shares.get(provider_name, 0)
            prev_share = self._previous_market_shares.get(provider_name, curr_share)
            self._current_market_momentum[provider_name] = curr_share - prev_share
        self._previous_market_shares = dict(market_shares)

        # Record observation
        self.memory.append({
            "type": "observation",
            "round": round_num,
            "leaderboard": leaderboard,
            "avg_satisfaction": consumer_data.get("avg_satisfaction"),
            "interventions": len(policymaker_data.get("interventions", [])),
        })

    def _get_provider_satisfaction(
        self,
        provider_name: str,
        consumer_data: dict,
    ) -> Optional[float]:
        """
        Get average satisfaction for a provider from consumer market data.

        Supports both new format (provider_satisfaction dict) and legacy
        format (individual subscriptions/satisfaction).

        Args:
            provider_name: Provider to get satisfaction for
            consumer_data: Consumer data from the round

        Returns:
            Average satisfaction or None if no data
        """
        if not consumer_data:
            return None

        # New format: direct per-provider satisfaction
        provider_sat = consumer_data.get("provider_satisfaction", {})
        if provider_sat and provider_name in provider_sat:
            return provider_sat[provider_name]

        # Fallback to overall average
        return consumer_data.get("avg_satisfaction")

    def reflect(self):
        """
        Reflect on observations and update beliefs about providers.

        Consider:
        - ROI from previous funding decisions
        - Provider performance trends
        - Gaming indicators
        """
        # Calculate ROI if we have active funding and history
        if self.private_state.active_funding and len(self.memory) > 1:
            # Simple ROI: score improvement of funded providers
            roi = 0.0
            funded_count = 0
            for provider, amount in self.private_state.active_funding.items():
                if provider in self.private_state.believed_provider_quality:
                    # ROI based on quality improvement (not just score)
                    quality = self.private_state.believed_provider_quality[provider]
                    roi += quality * (amount / self.private_state.total_capital)
                    funded_count += 1

            if funded_count > 0:
                roi = roi / funded_count
                self.private_state.roi_history.append(
                    (self.public_state.current_round, roi)
                )

        # Update industry trust based on gaming levels
        avg_gaming = 0
        if self.private_state.believed_provider_gaming:
            avg_gaming = sum(self.private_state.believed_provider_gaming.values()) / len(
                self.private_state.believed_provider_gaming
            )

        self.memory.append({
            "type": "reflection",
            "round": self.public_state.current_round,
            "avg_believed_gaming": avg_gaming,
            "beliefs": dict(self.private_state.believed_provider_quality),
        })

    def plan(self) -> dict:
        """
        Decide funding allocations for the next round.

        Respects funding_cooldown: if fewer than `funding_cooldown` rounds
        have passed since last allocation, returns previous allocations.

        Returns:
            Dict mapping provider names to funding amounts
        """
        current_round = self.public_state.current_round
        if current_round - self._last_funding_round < self.funding_cooldown:
            # Reuse previous allocations (no new decision)
            return dict(self.private_state.active_funding)

        self._last_funding_round = current_round

        if self.llm_mode:
            return self._plan_llm()
        else:
            return self._plan_heuristic()

    def _plan_heuristic(self) -> dict:
        """
        Heuristic funding decision based on funder type.

        Returns:
            Dict mapping provider names to funding amounts
        """
        if not self._last_leaderboard:
            return {}

        providers = [name for name, _ in self._last_leaderboard]
        allocations = {}

        available_capital = self.private_state.total_capital * self.max_round_deployment

        if self.funder_type == "vc":
            allocations = self._plan_vc(providers, available_capital)
        elif self.funder_type == "gov":
            allocations = self._plan_gov(providers, available_capital)
        elif self.funder_type == "foundation":
            allocations = self._plan_foundation(providers, available_capital)
        else:
            # Default: spread evenly
            per_provider = available_capital / len(providers)
            allocations = {p: per_provider for p in providers}

        # Build a short reasoning summary
        top_provider = max(allocations, key=allocations.get) if allocations else "none"
        top_amount = allocations.get(top_provider, 0) if allocations else 0
        reason = (
            f"{self.funder_type} strategy: top allocation "
            f"${top_amount:,.0f} to {top_provider}"
        )

        self.memory.append({
            "type": "planning",
            "round": self.public_state.current_round,
            "funder_type": self.funder_type,
            "allocations": allocations,
            "reason": reason,
        })

        return allocations

    def _get_score_momentum(self, provider: str) -> float:
        """Average score delta over last 3 rounds for a provider."""
        if len(self._score_history) < 2:
            return 0.0
        deltas = []
        for i in range(1, len(self._score_history)):
            prev = self._score_history[i - 1].get(provider)
            curr = self._score_history[i].get(provider)
            if prev is not None and curr is not None:
                deltas.append(curr - prev)
        return sum(deltas) / len(deltas) if deltas else 0.0

    def _compute_portfolio_concentration(self, provider: str) -> float:
        """
        Compute how concentrated other funders are on this provider.

        Returns:
            Value 0-1 where 1 = highly concentrated (all funders funding it)
        """
        if not self._other_funder_allocations:
            return 0.0  # No concentration data available

        total_funders = len(self._other_funder_allocations)
        if total_funders == 0:
            return 0.0

        # Count how many other funders are funding this provider
        funders_funding_provider = 0
        for funder_name, allocations in self._other_funder_allocations.items():
            if provider in allocations and allocations[provider] > 0:
                funders_funding_provider += 1

        # Concentration = fraction of other funders funding this provider
        return funders_funding_provider / total_funders

    def _score_providers(self, providers: list, weights: dict) -> dict:
        """Score providers using publicly observable momentum signals.

        Args:
            providers: List of provider names
            weights: dict with keys quality, score_momentum, market_traction, market_momentum, diversification

        Returns:
            Dict of {provider: composite_score}
        """
        market_shares = self._last_consumer_data.get("market_shares", {})
        scores = {}
        for provider in providers:
            quality = self.private_state.believed_provider_quality.get(provider, 0.5)
            score_mom = self._get_score_momentum(provider)
            traction = market_shares.get(provider, 0)
            market_mom = getattr(self, "_current_market_momentum", {}).get(provider, 0)

            # Diversification signal: high concentration reduces score
            concentration = self._compute_portfolio_concentration(provider)
            diversification_score = 1.0 - concentration  # Higher when less concentrated

            composite = (
                weights["quality"] * quality
                + weights["score_momentum"] * score_mom * 10  # Scale: deltas ~0.01-0.05
                + weights["market_traction"] * traction
                + weights["market_momentum"] * market_mom * 10
                + weights.get("diversification", 0.0) * diversification_score
            )
            scores[provider] = max(0, composite)
        return scores

    def _plan_vc(self, providers: list, capital: float) -> dict:
        """
        VC strategy: Back top performers, high concentration.

        Uses momentum signals — gaming effects emerge indirectly through
        declining market traction when scores don't match real quality.
        Includes diversification signal to avoid over-saturated opportunities.
        """
        scores = self._score_providers(providers, {
            "quality": 0.20, "score_momentum": 0.25,
            "market_traction": 0.20, "market_momentum": 0.20,
            "diversification": 0.15,
        })

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        allocations = {}

        # Concentrate funding on top performers
        if len(ranked) >= 2:
            allocations[ranked[0][0]] = capital * 0.6
            allocations[ranked[1][0]] = capital * 0.3
            remaining = capital * 0.1
            other_count = len(ranked) - 2
            if other_count > 0:
                per_other = remaining / other_count
                for provider, _ in ranked[2:]:
                    allocations[provider] = per_other
        elif len(ranked) == 1:
            allocations[ranked[0][0]] = capital

        return allocations

    def _plan_gov(self, providers: list, capital: float) -> dict:
        """
        Government/AISI strategy: Safety & stability, spread funding.

        Weights quality heavily, with moderate market traction signal.
        Gaming effects surface indirectly through low market share or
        declining traction when consumers notice quality gaps.
        Moderate diversification to support ecosystem stability.
        """
        scores = self._score_providers(providers, {
            "quality": 0.50, "score_momentum": 0.10,
            "market_traction": 0.25, "market_momentum": 0.05,
            "diversification": 0.10,
        })

        # Penalize providers with active regulatory interventions
        interventions = self._last_policymaker_data.get("interventions", [])
        if interventions:
            for provider in providers:
                scores[provider] = max(0, scores.get(provider, 0) - 0.1)

        # Normalize and allocate
        total_score = sum(scores.values())
        if total_score > 0:
            allocations = {p: (scores[p] / total_score) * capital for p in providers}
        else:
            per_provider = capital / len(providers)
            allocations = {p: per_provider for p in providers}

        return allocations

    def _plan_foundation(self, providers: list, capital: float) -> dict:
        """
        Foundation strategy: Mission alignment, reward capability growth.

        Balances quality with score momentum (genuine improvement).
        Gaming effects emerge indirectly: gaming providers have high scores
        but stalling momentum and declining market traction.
        Includes underdog bonus and strong diversification to support ecosystem health.
        """
        scores = self._score_providers(providers, {
            "quality": 0.35, "score_momentum": 0.20,
            "market_traction": 0.15, "market_momentum": 0.10,
            "diversification": 0.20,
        })

        # Underdog bonus: lower quality providers get a boost
        for provider in providers:
            quality = self.private_state.believed_provider_quality.get(provider, 0.5)
            scores[provider] = scores.get(provider, 0) + (1 - quality) * 0.15

        # Normalize and allocate
        total_score = sum(scores.values())
        if total_score > 0:
            allocations = {p: (scores[p] / total_score) * capital for p in providers}
        else:
            per_provider = capital / len(providers)
            allocations = {p: per_provider for p in providers}

        return allocations

    def _plan_llm(self) -> dict:
        """LLM-driven funding decision."""
        try:
            from llm import llm_plan_funding
            capped_capital = self.private_state.total_capital * self.max_round_deployment
            allocations, reasoning = llm_plan_funding(
                name=self.name,
                funder_type=self.funder_type,
                total_capital=capped_capital,
                believed_provider_quality=self.private_state.believed_provider_quality,
                believed_provider_gaming=self.private_state.believed_provider_gaming,
                leaderboard=self._last_leaderboard,
                consumer_satisfaction=self._last_consumer_data.get("avg_satisfaction"),
                recent_history=self.private_state.funding_history[-5:],
                verbose=False,
            )

            self.memory.append({
                "type": "planning_llm",
                "round": self.public_state.current_round,
                "reasoning": reasoning,
                "allocations": allocations,
            })

            return allocations
        except Exception as e:
            # Fallback to heuristic
            print(f"LLM planning failed: {e}, falling back to heuristic")
            return self._plan_heuristic()

    def execute(self, allocations: Optional[dict] = None):
        """
        Execute funding allocations.

        Args:
            allocations: Funding allocations (uses plan() result if None)
        """
        if allocations is None:
            allocations = self.plan()

        # Update active funding
        self.private_state.active_funding = allocations

        # Track deployed capital
        self.private_state.deployed_capital = sum(allocations.values())

        # Record in history
        self.private_state.funding_history.append(
            (self.public_state.current_round, dict(allocations))
        )

        # Public announcement (store in published_scores for simplicity)
        funded_providers = list(allocations.keys())
        if funded_providers:
            announcement = f"Round {self.public_state.current_round}: Funded {', '.join(funded_providers)}"
            self.public_state.published_scores.append(
                (self.public_state.current_round, announcement)
            )

        self.memory.append({
            "type": "execution",
            "round": self.public_state.current_round,
            "allocations": allocations,
            "total_deployed": self.private_state.deployed_capital,
        })

    def get_funding_multiplier(self, provider_name: str) -> float:
        """
        Get the funding multiplier for a provider.

        Multiplier ranges from 1.0 (no funding) to 2.0 (max funding).
        Based on the proportion of total capital allocated to the provider.

        Args:
            provider_name: Name of the provider

        Returns:
            Funding multiplier (1.0 - 2.0)
        """
        if not self.private_state.active_funding:
            return 1.0

        funding = self.private_state.active_funding.get(provider_name, 0)
        if funding <= 0:
            return 1.0

        # Multiplier based on funding proportion
        # Max funding (100% of capital) = 2.0x multiplier
        # No funding = 1.0x multiplier
        proportion = funding / self.private_state.total_capital
        multiplier = 1.0 + proportion

        # Cap at 2.0
        return min(2.0, multiplier)

    def get_prompt_context(self) -> str:
        """
        Get context for LLM prompts.

        Returns only public + private state, never ground truth.
        """
        context = "=== FUNDER STATE ===\n"
        context += f"Name: {self.name}\n"
        context += f"Type: {self.funder_type}\n"
        context += f"Mission: {self.private_state.mission_statement or 'N/A'}\n"
        context += f"Total Capital: ${self.private_state.total_capital:,.0f}\n"
        context += f"Deployed: ${self.private_state.deployed_capital:,.0f}\n"
        context += "\n"

        if self.private_state.believed_provider_quality:
            context += "Provider Assessments:\n"
            for name, quality in sorted(
                self.private_state.believed_provider_quality.items(),
                key=lambda x: x[1],
                reverse=True
            ):
                gaming = self.private_state.believed_provider_gaming.get(name, 0)
                context += f"  {name}: quality={quality:.2f}, gaming_risk={gaming:.2f}\n"

        if self.private_state.active_funding:
            context += "\nCurrent Funding:\n"
            for name, amount in self.private_state.active_funding.items():
                context += f"  {name}: ${amount:,.0f}\n"

        if self.private_state.roi_history:
            context += "\nRecent ROI:\n"
            for round_num, roi in self.private_state.roi_history[-5:]:
                context += f"  Round {round_num}: {roi:.2%}\n"

        return context

    def save(self, folder: str):
        """Save funder state to a folder."""
        os.makedirs(folder, exist_ok=True)

        with open(f"{folder}/public_state.json", "w") as f:
            json.dump(self.public_state.to_dict(), f, indent=2)

        with open(f"{folder}/private_state.json", "w") as f:
            json.dump(self.private_state.to_dict(), f, indent=2)

        with open(f"{folder}/memory.json", "w") as f:
            json.dump(self.memory, f, indent=2)

        # Save parameters
        with open(f"{folder}/params.json", "w") as f:
            json.dump({
                "risk_tolerance": self.risk_tolerance,
                "llm_mode": self.llm_mode,
                "max_round_deployment": self.max_round_deployment,
                "funding_cooldown": self.funding_cooldown,
            }, f, indent=2)

    @classmethod
    def load(cls, folder: str) -> "Funder":
        """Load funder state from a folder."""
        with open(f"{folder}/params.json", "r") as f:
            params = json.load(f)

        with open(f"{folder}/public_state.json", "r") as f:
            public_data = json.load(f)

        with open(f"{folder}/private_state.json", "r") as f:
            private_data = json.load(f)

        funder = cls(
            name=public_data["name"],
            funder_type=private_data.get("funder_type", "vc"),
            total_capital=private_data.get("total_capital", 1000000.0),
            mission_statement=private_data.get("mission_statement", ""),
            risk_tolerance=params.get("risk_tolerance", 0.5),
            llm_mode=params.get("llm_mode", False),
            max_round_deployment=params.get("max_round_deployment", 0.10),
            funding_cooldown=params.get("funding_cooldown", 2),
        )

        funder.public_state = PublicState.from_dict(public_data)
        funder.private_state = FunderPrivateState.from_dict(private_data)

        with open(f"{folder}/memory.json", "r") as f:
            funder.memory = json.load(f)

        return funder

    def __repr__(self):
        return (
            f"Funder(name='{self.name}', "
            f"type='{self.funder_type}', "
            f"deployed=${self.private_state.deployed_capital:,.0f})"
        )


def get_default_funder_configs() -> list[dict]:
    """
    Get default funder configuration (1 VC funder).

    Returns:
        List with single VC funder config
    """
    return [
        {
            "name": "TechVentures",
            "funder_type": "vc",
            "total_capital": 1000000.0,
            "risk_tolerance": 0.7,
            "mission_statement": "Maximize returns by backing AI market leaders",
        },
    ]


def get_multi_funder_configs() -> list[dict]:
    """
    Get multi-funder configuration with all three types.

    Returns:
        List with VC, Government, and Foundation funder configs
    """
    return [
        {
            "name": "TechVentures",
            "funder_type": "vc",
            "total_capital": 1000000.0,
            "risk_tolerance": 0.7,
            "mission_statement": "Maximize returns by backing AI market leaders",
        },
        {
            "name": "AISI_Fund",
            "funder_type": "gov",
            "total_capital": 500000.0,
            "risk_tolerance": 0.3,
            "mission_statement": "Ensure safe and responsible AI development",
        },
        {
            "name": "OpenResearch",
            "funder_type": "foundation",
            "total_capital": 300000.0,
            "risk_tolerance": 0.5,
            "mission_statement": "Support authentic capability advancement for societal benefit",
        },
    ]
