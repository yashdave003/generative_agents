"""
Consumer Actor for Evaluation Ecosystem Simulation

Represents an individual end user who decides which model to use based on
leaderboard rankings and their actual experience with the model.

Key dynamics:
- Consumers observe leaderboard rankings
- They subscribe to models based on perceived quality
- Their actual satisfaction depends on true_capability (not score)
- Gaming creates a satisfaction gap: high score but low true capability = disappointed users
- Consumers may switch providers when dissatisfied

Visibility:
- PUBLIC: name, current_subscription
- PRIVATE: believed_model_quality, use_cases, budget, satisfaction_history
- INVISIBLE: true_satisfaction (how well model actually serves them)
"""
import json
import os
from dataclasses import dataclass, field
from typing import Optional

from visibility import PublicState, ConsumerPrivateState, ConsumerGroundTruth


class Consumer:
    """
    A Consumer agent in the evaluation ecosystem simulation.

    Consumers are end users who:
    1. Observe benchmark leaderboards
    2. Choose which model to subscribe to
    3. Experience actual satisfaction based on true model capability
    4. May switch models if dissatisfied

    This creates demand-side feedback: if gaming leads to poor real-world
    performance, consumers become dissatisfied and switch providers.

    Visibility Model:
    - public_state: Visible to all (name, subscription)
    - private_state: Visible only to self (beliefs, budget, history)
    - ground_truth: Held by simulation (true_satisfaction)
    """

    def __init__(
        self,
        name: str,
        use_cases: list[str] = None,
        budget: float = 100.0,
        quality_sensitivity: float = 0.5,
        switching_threshold: float = 0.3,
        leaderboard_trust: float = 0.7,
        switching_cost: float = 0.1,
        llm_mode: bool = False,
    ):
        """
        Initialize a Consumer.

        Args:
            name: Unique identifier for this consumer
            use_cases: List of use cases (e.g., ["coding", "writing"])
            budget: Monthly budget for subscriptions
            quality_sensitivity: How much quality affects their satisfaction (0-1)
            switching_threshold: How much dissatisfaction before switching (0-1)
            leaderboard_trust: How much to trust leaderboard vs own experience (0-1)
            switching_cost: Additional threshold penalty for switching providers (0-1)
            llm_mode: If True, use LLM for decision-making
        """
        # Initialize public state
        self.public_state = PublicState(
            name=name,
            current_round=0,
            published_scores=[],
        )

        # Initialize private state
        self.private_state = ConsumerPrivateState(
            use_cases=use_cases or ["general"],
            budget=budget,
            current_subscription=None,
            believed_model_quality={},
            satisfaction_history=[],
            subscription_history=[],
            leaderboard_trust=leaderboard_trust,
            switching_cost=switching_cost,
        )

        # Consumer-specific parameters
        self.quality_sensitivity = quality_sensitivity
        self.switching_threshold = switching_threshold
        self.llm_mode = llm_mode

        # Memory
        self.memory = []

        # Last observed leaderboard
        self._last_leaderboard: list = []

        # Brand recognition factors (set externally by simulation)
        self._brand_recognition: dict = {}

    @property
    def name(self) -> str:
        return self.public_state.name

    def observe(self, leaderboard: list, round_num: int):
        """
        Observe the current leaderboard.

        Args:
            leaderboard: List of (provider_name, score) tuples, sorted by score
            round_num: Current simulation round
        """
        self.public_state.current_round = round_num
        self._last_leaderboard = leaderboard

        # Update beliefs about model quality based on leaderboard
        for provider_name, score in leaderboard:
            # New providers start with score as belief
            if provider_name not in self.private_state.believed_model_quality:
                self.private_state.believed_model_quality[provider_name] = score
            else:
                # Update belief with learning rate
                learning_rate = 0.3
                old_belief = self.private_state.believed_model_quality[provider_name]
                self.private_state.believed_model_quality[provider_name] = (
                    (1 - learning_rate) * old_belief + learning_rate * score
                )

        # Record observation
        self.memory.append({
            "type": "observation",
            "round": round_num,
            "leaderboard": leaderboard,
        })

    def reflect(self):
        """
        Reflect on recent experience and update beliefs.

        If subscribed to a model, compare experienced satisfaction with expectations.
        """
        if not self.private_state.satisfaction_history:
            return

        # Get recent satisfaction
        recent = self.private_state.satisfaction_history[-3:]
        if not recent:
            return

        current_sub = self.private_state.current_subscription
        if not current_sub:
            return

        # Calculate average recent satisfaction with current provider
        recent_with_current = [
            sat for _, provider, sat in recent if provider == current_sub
        ]

        if recent_with_current:
            avg_satisfaction = sum(recent_with_current) / len(recent_with_current)

            # Update belief about current provider based on experience
            # This is where gaming gets exposed: if true_capability < score,
            # actual experience will be disappointing
            expected_quality = self.private_state.believed_model_quality.get(current_sub, 0.5)
            experience_weight = 0.4

            # Blend benchmark belief with actual experience
            self.private_state.believed_model_quality[current_sub] = (
                (1 - experience_weight) * expected_quality +
                experience_weight * avg_satisfaction
            )

        self.memory.append({
            "type": "reflection",
            "round": self.public_state.current_round,
            "beliefs": dict(self.private_state.believed_model_quality),
        })

    def plan(self) -> Optional[str]:
        """
        Decide whether to subscribe, switch, or stay with current provider.

        Returns:
            Provider name to subscribe to, or None to unsubscribe
        """
        if self.llm_mode:
            return self._plan_llm()
        else:
            return self._plan_heuristic()

    def _blended_score(self, provider_name: str, lb_score: float) -> float:
        """Compute blended perceived quality for a provider."""
        trust = self.private_state.leaderboard_trust
        brand_factor = self._brand_recognition.get(provider_name, 0.5)
        default_belief = lb_score * brand_factor
        believed = self.private_state.believed_model_quality.get(
            provider_name, default_belief
        )
        return trust * lb_score + (1 - trust) * believed

    def _plan_heuristic(self) -> Optional[str]:
        """Heuristic subscription decision with switching costs and blended scoring.

        Two switching triggers:
        1. Dissatisfaction (Goodhart signal): leaderboard score promised more
           than the consumer actually experienced.
        2. Opportunity: a clearly better-scoring alternative appears on the
           leaderboard, exceeding the switching cost + inertia.
        """
        current_sub = self.private_state.current_subscription
        should_switch = False
        switch_reason = ""

        if current_sub and self._last_leaderboard:
            tenure_bonus = min(0.1, self.private_state.rounds_with_provider * 0.02)

            # --- Trigger 1: Dissatisfaction (Goodhart signal) ---
            # Fires when leaderboard score (promise) exceeds actual
            # satisfaction (reality) by more than the threshold.
            if self.private_state.satisfaction_history:
                recent = [
                    sat for _, provider, sat in self.private_state.satisfaction_history[-3:]
                    if provider == current_sub
                ]
                if recent:
                    avg_satisfaction = sum(recent) / len(recent)
                    leaderboard_expected = next(
                        (score for name, score in self._last_leaderboard
                         if name == current_sub),
                        None,
                    )
                    if leaderboard_expected is None:
                        leaderboard_expected = self.private_state.believed_model_quality.get(
                            current_sub, 0.5
                        )

                    satisfaction_gap = leaderboard_expected - avg_satisfaction
                    dissatisfaction_threshold = (
                        self.switching_threshold + tenure_bonus
                        + self.private_state.switching_cost
                    )
                    if satisfaction_gap > dissatisfaction_threshold:
                        should_switch = True
                        switch_reason = (
                            f"dissatisfied: gap={satisfaction_gap:.3f} "
                            f"> threshold={dissatisfaction_threshold:.3f}"
                        )

            # --- Trigger 2: Better alternative available ---
            # Even when not dissatisfied, consumers notice if another
            # provider's blended score is significantly better than their
            # current provider's.  This is basic market competition.
            if not should_switch:
                current_lb_score = next(
                    (s for n, s in self._last_leaderboard if n == current_sub),
                    None,
                )
                if current_lb_score is not None:
                    current_perceived = self._blended_score(
                        current_sub, current_lb_score
                    )
                    opportunity_threshold = (
                        self.private_state.switching_cost + tenure_bonus
                    )
                    for name, score in self._last_leaderboard:
                        if name == current_sub:
                            continue
                        alt_perceived = self._blended_score(name, score)
                        improvement = alt_perceived - current_perceived
                        if improvement > opportunity_threshold:
                            should_switch = True
                            switch_reason = (
                                f"better option: {name} "
                                f"(+{improvement:.3f} > {opportunity_threshold:.3f})"
                            )
                            break

        # If no subscription or considering switching, pick best option
        if should_switch or current_sub is None:
            if not self._last_leaderboard:
                return None

            best_score = -1
            best_provider = None
            for provider_name, lb_score in self._last_leaderboard:
                blended = self._blended_score(provider_name, lb_score)
                if blended > best_score:
                    best_score = blended
                    best_provider = provider_name

            self.memory.append({
                "type": "planning",
                "round": self.public_state.current_round,
                "decision": "switch" if current_sub else "subscribe",
                "provider": best_provider,
                "from": current_sub,
                "reason": switch_reason or "initial subscription",
            })

            return best_provider

        # Stay with current provider
        self.memory.append({
            "type": "planning",
            "round": self.public_state.current_round,
            "decision": "stay",
            "provider": current_sub,
            "reason": "satisfied with current provider",
        })

        return current_sub

    def _plan_llm(self) -> Optional[str]:
        """LLM-driven subscription decision (future implementation)."""
        # For now, fall back to heuristic
        return self._plan_heuristic()

    def execute(self, new_subscription: Optional[str] = None):
        """
        Execute subscription decision.

        Args:
            new_subscription: Provider to subscribe to (uses plan() result if None)
        """
        if new_subscription is None:
            new_subscription = self.plan()

        old_sub = self.private_state.current_subscription

        # Track switch
        if old_sub != new_subscription:
            self.memory.append({
                "type": "subscription_change",
                "round": self.public_state.current_round,
                "from": old_sub,
                "to": new_subscription,
            })

        self.private_state.current_subscription = new_subscription

        if new_subscription:
            self.private_state.subscription_history.append(
                (self.public_state.current_round, new_subscription)
            )

    def receive_satisfaction(self, satisfaction: float):
        """
        Receive actual satisfaction from using the model.

        This is called by the simulation based on ground truth.

        Args:
            satisfaction: Actual satisfaction level (0-1)
        """
        current_sub = self.private_state.current_subscription
        if current_sub:
            self.private_state.satisfaction_history.append(
                (self.public_state.current_round, current_sub, satisfaction)
            )

    def get_prompt_context(self) -> str:
        """
        Get context for LLM prompts.

        Returns only public + private state, never ground truth.
        """
        context = "=== CONSUMER STATE ===\n"
        context += f"Name: {self.name}\n"
        context += f"Current Subscription: {self.private_state.current_subscription or 'None'}\n"
        context += f"Budget: ${self.private_state.budget:.0f}/month\n"
        context += f"Use Cases: {', '.join(self.private_state.use_cases)}\n"
        context += "\n"

        if self.private_state.believed_model_quality:
            context += "Model Quality Beliefs:\n"
            for name, quality in sorted(
                self.private_state.believed_model_quality.items(),
                key=lambda x: x[1],
                reverse=True
            ):
                context += f"  {name}: {quality:.2f}\n"

        if self.private_state.satisfaction_history:
            context += "\nRecent Satisfaction:\n"
            for round_num, provider, sat in self.private_state.satisfaction_history[-5:]:
                context += f"  Round {round_num} ({provider}): {sat:.2f}\n"

        return context

    def save(self, folder: str):
        """Save consumer state to a folder."""
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
                "quality_sensitivity": self.quality_sensitivity,
                "switching_threshold": self.switching_threshold,
                "llm_mode": self.llm_mode,
                "brand_recognition": self._brand_recognition,
            }, f, indent=2)

    @classmethod
    def load(cls, folder: str) -> "Consumer":
        """Load consumer state from a folder."""
        with open(f"{folder}/params.json", "r") as f:
            params = json.load(f)

        with open(f"{folder}/public_state.json", "r") as f:
            public_data = json.load(f)

        with open(f"{folder}/private_state.json", "r") as f:
            private_data = json.load(f)

        consumer = cls(
            name=public_data["name"],
            use_cases=private_data.get("use_cases", ["general"]),
            budget=private_data.get("budget", 100.0),
            quality_sensitivity=params.get("quality_sensitivity", 0.5),
            switching_threshold=params.get("switching_threshold", 0.3),
            leaderboard_trust=private_data.get("leaderboard_trust", 0.7),
            switching_cost=private_data.get("switching_cost", 0.1),
            llm_mode=params.get("llm_mode", False),
        )
        consumer._brand_recognition = params.get("brand_recognition", {})

        consumer.public_state = PublicState.from_dict(public_data)
        consumer.private_state = ConsumerPrivateState.from_dict(private_data)

        with open(f"{folder}/memory.json", "r") as f:
            consumer.memory = json.load(f)

        return consumer

    def __repr__(self):
        return (
            f"Consumer(name='{self.name}', "
            f"subscription='{self.private_state.current_subscription}')"
        )
