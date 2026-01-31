"""
Policymaker Actor for Evaluation Ecosystem Simulation

Represents a regulator who can mandate evaluations, set requirements,
and respond to incidents in the AI ecosystem.

Key dynamics:
- Policymakers observe leaderboard, consumer satisfaction, and incidents
- They can issue regulations that change benchmark behavior
- Their interventions create constraints for providers
- They respond to signs of gaming (validity correlation dropping)

Visibility:
- PUBLIC: name, active_regulations, public_statements
- PRIVATE: policy_objectives, risk_beliefs, regulatory_capacity
- INVISIBLE: true_risk_tolerance, true_intervention_effectiveness
"""
import json
import os
from dataclasses import dataclass, field
from typing import Optional

from visibility import PublicState, PolicymakerPrivateState, PolicymakerGroundTruth


class Policymaker:
    """
    A Policymaker agent in the evaluation ecosystem simulation.

    Policymakers are regulators who:
    1. Observe ecosystem state (leaderboard, consumer satisfaction, validity)
    2. Assess risks and identify problems
    3. Issue regulations to change provider/evaluator behavior
    4. Monitor compliance and outcomes

    This creates regulatory pressure: if gaming becomes apparent,
    policymakers can mandate changes that affect provider strategies.

    Visibility Model:
    - public_state: Visible to all (name, regulations, statements)
    - private_state: Visible only to self (objectives, beliefs, capacity)
    - ground_truth: Held by simulation (true effectiveness)
    """

    def __init__(
        self,
        name: str,
        policy_objectives: list[str] = None,
        intervention_threshold: float = 0.3,
        risk_tolerance: float = 0.5,
        llm_mode: bool = False,
    ):
        """
        Initialize a Policymaker.

        Args:
            name: Unique identifier for this policymaker
            policy_objectives: List of objectives (e.g., ["safety", "fairness"])
            intervention_threshold: How much concern before intervening (0-1)
            risk_tolerance: How much risk is acceptable (0-1)
            llm_mode: If True, use LLM for decision-making
        """
        # Initialize public state
        self.public_state = PublicState(
            name=name,
            current_round=0,
            published_scores=[],  # Reused for public statements
        )

        # Initialize private state
        self.private_state = PolicymakerPrivateState(
            policy_objectives=policy_objectives or ["safety", "fairness"],
            risk_beliefs={
                "gaming_risk": 0.3,  # Belief about gaming prevalence
                "consumer_harm_risk": 0.3,  # Belief about consumer harm
                "validity_degradation_risk": 0.3,  # Belief about benchmark validity loss
            },
            industry_trust=0.5,
            regulatory_capacity=1.0,
            past_interventions=[],
            observed_incidents=[],
        )

        # Policymaker-specific parameters
        self.intervention_threshold = intervention_threshold
        self.risk_tolerance = risk_tolerance
        self.llm_mode = llm_mode

        # Memory
        self.memory = []

        # Tracking
        self._last_validity_correlation: Optional[float] = None
        self._last_consumer_satisfaction: Optional[float] = None

    @property
    def name(self) -> str:
        return self.public_state.name

    def observe(
        self,
        leaderboard: list,
        consumer_satisfaction: Optional[float],
        validity_correlation: Optional[float],
        round_num: int,
    ):
        """
        Observe the current ecosystem state.

        Args:
            leaderboard: List of (provider_name, score) tuples
            consumer_satisfaction: Average consumer satisfaction (0-1)
            validity_correlation: Correlation between scores and true capability
            round_num: Current simulation round
        """
        self.public_state.current_round = round_num

        # Track metrics over time
        self._last_validity_correlation = validity_correlation
        self._last_consumer_satisfaction = consumer_satisfaction

        # Update risk beliefs based on observations
        if validity_correlation is not None:
            # Low validity correlation suggests gaming
            if validity_correlation < 0.5:
                self.private_state.risk_beliefs["gaming_risk"] = min(
                    1.0,
                    self.private_state.risk_beliefs["gaming_risk"] + 0.1
                )
                self.private_state.risk_beliefs["validity_degradation_risk"] = min(
                    1.0,
                    self.private_state.risk_beliefs["validity_degradation_risk"] + 0.1
                )
            else:
                # High correlation is reassuring
                self.private_state.risk_beliefs["gaming_risk"] = max(
                    0.0,
                    self.private_state.risk_beliefs["gaming_risk"] - 0.05
                )

        if consumer_satisfaction is not None:
            # Low satisfaction suggests consumer harm
            if consumer_satisfaction < 0.5:
                self.private_state.risk_beliefs["consumer_harm_risk"] = min(
                    1.0,
                    self.private_state.risk_beliefs["consumer_harm_risk"] + 0.1
                )
                # Record as incident
                self.private_state.observed_incidents.append(
                    (round_num, f"Low consumer satisfaction: {consumer_satisfaction:.2f}")
                )
            else:
                self.private_state.risk_beliefs["consumer_harm_risk"] = max(
                    0.0,
                    self.private_state.risk_beliefs["consumer_harm_risk"] - 0.05
                )

        # Record observation
        self.memory.append({
            "type": "observation",
            "round": round_num,
            "validity_correlation": validity_correlation,
            "consumer_satisfaction": consumer_satisfaction,
            "risk_beliefs": dict(self.private_state.risk_beliefs),
        })

    def reflect(self):
        """
        Reflect on observations and update policy stance.

        Consider whether current regulations are effective and
        whether new interventions are needed.
        """
        # Update industry trust based on risk beliefs
        avg_risk = sum(self.private_state.risk_beliefs.values()) / len(
            self.private_state.risk_beliefs
        )

        # High risk beliefs reduce trust
        trust_adjustment = 0.1 * (self.risk_tolerance - avg_risk)
        self.private_state.industry_trust = max(
            0.0,
            min(1.0, self.private_state.industry_trust + trust_adjustment)
        )

        self.memory.append({
            "type": "reflection",
            "round": self.public_state.current_round,
            "industry_trust": self.private_state.industry_trust,
            "avg_risk": avg_risk,
        })

    def plan(self) -> Optional[dict]:
        """
        Decide whether to issue a regulatory intervention.

        Returns:
            Intervention dict with type and details, or None if no intervention
        """
        if self.llm_mode:
            return self._plan_llm()
        else:
            return self._plan_heuristic()

    def _plan_heuristic(self) -> Optional[dict]:
        """Heuristic intervention decision."""
        # Check if any risk exceeds threshold
        max_risk = max(self.private_state.risk_beliefs.values())

        if max_risk <= self.intervention_threshold:
            return None  # No intervention needed

        # Determine intervention type based on highest risk
        risks = self.private_state.risk_beliefs
        intervention = None

        # Validity degradation -> mandate stronger benchmark
        if risks["validity_degradation_risk"] == max_risk:
            if self._last_validity_correlation and self._last_validity_correlation < 0.4:
                intervention = {
                    "type": "mandate_benchmark",
                    "name": f"Validity_Mandate_R{self.public_state.current_round}",
                    "details": {
                        "validity": min(0.9, 0.7 + 0.1),  # Increase validity requirement
                        "exploitability": max(0.2, 0.5 - 0.2),  # Decrease exploitability
                    },
                    "reason": f"Validity correlation dropped to {self._last_validity_correlation:.2f}",
                }

        # Consumer harm -> require disclosure or set thresholds
        elif risks["consumer_harm_risk"] == max_risk:
            if self._last_consumer_satisfaction and self._last_consumer_satisfaction < 0.4:
                intervention = {
                    "type": "require_disclosure",
                    "name": f"Disclosure_Mandate_R{self.public_state.current_round}",
                    "details": {
                        "require_capability_disclosure": True,
                        "require_gaming_disclosure": True,
                    },
                    "reason": f"Consumer satisfaction dropped to {self._last_consumer_satisfaction:.2f}",
                }

        # Gaming risk -> increase benchmark requirements
        elif risks["gaming_risk"] == max_risk:
            intervention = {
                "type": "mandate_benchmark",
                "name": f"Anti_Gaming_R{self.public_state.current_round}",
                "details": {
                    "exploitability": max(0.1, 0.5 - 0.3),  # Reduce exploitability
                },
                "reason": f"Gaming risk assessment: {risks['gaming_risk']:.2f}",
            }

        if intervention:
            self.memory.append({
                "type": "planning",
                "round": self.public_state.current_round,
                "decision": "intervene",
                "intervention": intervention,
            })
        else:
            self.memory.append({
                "type": "planning",
                "round": self.public_state.current_round,
                "decision": "no_action",
                "reason": "risks below threshold",
            })

        return intervention

    def _plan_llm(self) -> Optional[dict]:
        """LLM-driven intervention decision (future implementation)."""
        # For now, fall back to heuristic
        return self._plan_heuristic()

    def execute(self, intervention: Optional[dict] = None):
        """
        Execute a regulatory intervention.

        Args:
            intervention: Intervention to execute (uses plan() result if None)
        """
        if intervention is None:
            intervention = self.plan()

        if intervention is None:
            return

        # Record intervention
        self.private_state.past_interventions.append(
            (
                self.public_state.current_round,
                intervention["type"],
                intervention.get("details", {}),
            )
        )

        # Public statement (stored in published_scores for simplicity)
        statement = f"[Round {self.public_state.current_round}] Issued {intervention['type']}: {intervention.get('reason', 'N/A')}"
        self.public_state.published_scores.append(
            (self.public_state.current_round, statement)
        )

        self.memory.append({
            "type": "execution",
            "round": self.public_state.current_round,
            "intervention": intervention,
        })

    def get_active_interventions(self) -> list[tuple]:
        """Get list of past interventions."""
        return self.private_state.past_interventions

    def get_prompt_context(self) -> str:
        """
        Get context for LLM prompts.

        Returns only public + private state, never ground truth.
        """
        context = "=== POLICYMAKER STATE ===\n"
        context += f"Name: {self.name}\n"
        context += f"Policy Objectives: {', '.join(self.private_state.policy_objectives)}\n"
        context += f"Industry Trust Level: {self.private_state.industry_trust:.2f}\n"
        context += f"Regulatory Capacity: {self.private_state.regulatory_capacity:.2f}\n"
        context += "\n"

        context += "Risk Assessments:\n"
        for risk, level in self.private_state.risk_beliefs.items():
            context += f"  {risk}: {level:.2f}\n"

        if self.private_state.past_interventions:
            context += "\nPast Interventions:\n"
            for round_num, intervention_type, details in self.private_state.past_interventions[-5:]:
                context += f"  Round {round_num}: {intervention_type} - {details}\n"

        if self.private_state.observed_incidents:
            context += "\nObserved Incidents:\n"
            for round_num, incident in self.private_state.observed_incidents[-5:]:
                context += f"  Round {round_num}: {incident}\n"

        return context

    def save(self, folder: str):
        """Save policymaker state to a folder."""
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
                "intervention_threshold": self.intervention_threshold,
                "risk_tolerance": self.risk_tolerance,
                "llm_mode": self.llm_mode,
            }, f, indent=2)

    @classmethod
    def load(cls, folder: str) -> "Policymaker":
        """Load policymaker state from a folder."""
        with open(f"{folder}/params.json", "r") as f:
            params = json.load(f)

        with open(f"{folder}/public_state.json", "r") as f:
            public_data = json.load(f)

        with open(f"{folder}/private_state.json", "r") as f:
            private_data = json.load(f)

        policymaker = cls(
            name=public_data["name"],
            policy_objectives=private_data.get("policy_objectives", ["safety"]),
            intervention_threshold=params.get("intervention_threshold", 0.3),
            risk_tolerance=params.get("risk_tolerance", 0.5),
            llm_mode=params.get("llm_mode", False),
        )

        policymaker.public_state = PublicState.from_dict(public_data)
        policymaker.private_state = PolicymakerPrivateState.from_dict(private_data)

        with open(f"{folder}/memory.json", "r") as f:
            policymaker.memory = json.load(f)

        return policymaker

    def __repr__(self):
        return (
            f"Policymaker(name='{self.name}', "
            f"trust={self.private_state.industry_trust:.2f})"
        )
