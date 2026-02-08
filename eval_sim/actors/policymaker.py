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

    def _detect_score_volatility(self) -> bool:
        """Detect suspicious score spikes (possible gaming signal)."""
        # Check if any provider's score jumped more than 0.1 in one round
        if len(self.memory) < 2:
            return False
        recent_obs = [m for m in self.memory if m.get("type") == "observation"]
        if len(recent_obs) < 2:
            return False
        # Compare leaderboard from last two observations
        last = recent_obs[-1]
        prev = recent_obs[-2]
        last_scores = {name: score for name, score in last.get("leaderboard", [])}
        prev_scores = {name: score for name, score in prev.get("leaderboard", [])}
        for name in last_scores:
            if name in prev_scores:
                if abs(last_scores[name] - prev_scores[name]) > 0.1:
                    return True
        return False

    def _detect_satisfaction_trend(self) -> bool:
        """Detect declining consumer satisfaction trend over last 3 observations."""
        recent_obs = [m for m in self.memory if m.get("type") == "observation" and m.get("consumer_satisfaction") is not None]
        if len(recent_obs) < 3:
            return False
        sats = [m["consumer_satisfaction"] for m in recent_obs[-3:]]
        # Declining if each is lower than the previous
        return sats[-1] < sats[-2] < sats[-3]

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
            "leaderboard": leaderboard,
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
        """Graduated escalation intervention decision.

        Escalation ladder: investigation -> public_warning -> mandate_benchmark -> compliance_audit
        Event-driven triggers: score volatility, declining satisfaction, risk thresholds.
        """
        max_risk = max(self.private_state.risk_beliefs.values())

        # Track escalation state from past interventions
        has_investigated = any(
            t == "investigation" for _, t, _ in self.private_state.past_interventions
        )
        has_warned = any(
            t == "public_warning" for _, t, _ in self.private_state.past_interventions
        )
        has_mandated = any(
            t == "mandate_benchmark" for _, t, _ in self.private_state.past_interventions
        )

        # Check how many rounds since last intervention of any type
        rounds_since_last_intervention = None
        rounds_since_mandate = None
        for r, t, _ in reversed(self.private_state.past_interventions):
            if rounds_since_last_intervention is None:
                rounds_since_last_intervention = self.public_state.current_round - r
            if t == "mandate_benchmark" and rounds_since_mandate is None:
                rounds_since_mandate = self.public_state.current_round - r

        # Cooldown: don't intervene again within 3 rounds of last intervention
        if rounds_since_last_intervention is not None and rounds_since_last_intervention < 3:
            self.memory.append({
                "type": "planning",
                "round": self.public_state.current_round,
                "decision": "no_action",
                "reason": f"cooldown: {rounds_since_last_intervention} rounds since last intervention",
            })
            return None

        # Detect events
        score_volatility = self._detect_score_volatility()
        satisfaction_declining = self._detect_satisfaction_trend()

        intervention = None

        # Compliance audit: mandate issued > 3 rounds ago and risk still high
        if has_mandated and rounds_since_mandate is not None and rounds_since_mandate > 3 and max_risk > 0.5:
            intervention = {
                "type": "compliance_audit",
                "name": f"Compliance_Audit_R{self.public_state.current_round}",
                "details": {
                    "exploitability_reduction": 0.1,
                },
                "reason": f"Risk still high ({max_risk:.2f}) after mandate {rounds_since_mandate} rounds ago",
            }
        # High risk + prior investigation -> mandate benchmark (only if not already mandated recently)
        elif max_risk > 0.6 and has_investigated and not has_mandated:
            intervention = {
                "type": "mandate_benchmark",
                "name": f"Benchmark_Mandate_R{self.public_state.current_round}",
                "details": {
                    "validity": min(0.9, 0.7 + 0.1),
                    "exploitability": max(0.2, 0.5 - 0.2),
                },
                "reason": f"High risk ({max_risk:.2f}) with prior investigation",
            }
        # Moderate risk or score volatility -> investigate or warn
        elif max_risk > 0.4 or score_volatility:
            if not has_investigated:
                intervention = {
                    "type": "investigation",
                    "name": f"Investigation_R{self.public_state.current_round}",
                    "details": {
                        "focus": "score_volatility" if score_volatility else "elevated_risk",
                    },
                    "reason": f"Score volatility detected" if score_volatility else f"Risk elevated ({max_risk:.2f})",
                }
            elif not has_warned:
                intervention = {
                    "type": "public_warning",
                    "name": f"Public_Warning_R{self.public_state.current_round}",
                    "details": {
                        "warning_severity": "moderate" if max_risk < 0.6 else "high",
                    },
                    "reason": f"Follow-up to investigation, risk at {max_risk:.2f}",
                }
        # Declining satisfaction -> investigate
        elif satisfaction_declining and not has_investigated:
            intervention = {
                "type": "investigation",
                "name": f"Satisfaction_Investigation_R{self.public_state.current_round}",
                "details": {
                    "focus": "consumer_satisfaction_decline",
                },
                "reason": "Consumer satisfaction declining over 3+ rounds",
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
                "reason": f"max_risk={max_risk:.2f}, below threshold or no escalation path",
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
