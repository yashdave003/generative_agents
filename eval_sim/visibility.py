"""
Visibility System for Evaluation Ecosystem Simulation

Implements three-tier visibility model:
- PUBLIC: Visible to all actors and logger
- PRIVATE: Visible only to self and logger
- INVISIBLE (GroundTruth): Only visible to simulation/logger, never to actors

Key Design Principle: Invisible state doesn't live inside the actor.
The simulation holds ground truth externally, making it structurally
impossible for LLM prompts to access it.
"""
import json
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PublicState:
    """
    State visible to all actors.

    This information can be freely shared in prompts and accessed by any actor.
    """
    name: str = ""
    current_round: int = 0
    # List of (round, score) tuples
    published_scores: list = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dict for serialization."""
        return {
            "name": self.name,
            "current_round": self.current_round,
            "published_scores": self.published_scores,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PublicState":
        """Create from dict."""
        return cls(**data)

    def get_summary(self) -> str:
        """Get human-readable summary for prompts."""
        summary = f"Name: {self.name}\n"
        summary += f"Current Round: {self.current_round}\n"
        if self.published_scores:
            recent = self.published_scores[-5:]
            summary += "Recent Scores:\n"
            for round_num, score in recent:
                summary += f"  Round {round_num}: {score:.3f}\n"
        else:
            summary += "No scores yet.\n"
        return summary


@dataclass
class ProviderPrivateState:
    """
    Private state for Model Provider actors.

    Only accessible to the owning actor and the logger.
    Competitors cannot see this state.
    """
    # Strategy profile and traits
    strategy_profile: str = ""
    innate_traits: str = ""

    # Belief state (uncertain estimates, updated over time)
    believed_own_capability: float = 0.5
    believed_benchmark_exploitability: float = 0.3
    capability_belief_confidence: float = 0.5
    believed_competitor_capabilities: dict = field(default_factory=dict)

    # Investment portfolio (decisions made each round)
    # These four investments must sum to effort_budget
    fundamental_research: float = 0.25  # Novel architectures, pre-training improvements
    training_optimization: float = 0.25  # Scaling, data quality, fine-tuning
    evaluation_engineering: float = 0.25  # Benchmark-specific optimization
    safety_alignment: float = 0.25  # RLHF, red-teaming, reliability
    effort_budget: float = 1.0

    # History tracking
    past_strategies: list = field(default_factory=list)  # [(round, rnd, gaming), ...]
    observed_competitor_scores: dict = field(default_factory=dict)  # {name: [(round, score), ...]}

    # Reflection state
    recent_insights: list = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dict for serialization."""
        return {
            "strategy_profile": self.strategy_profile,
            "innate_traits": self.innate_traits,
            "believed_own_capability": self.believed_own_capability,
            "believed_benchmark_exploitability": self.believed_benchmark_exploitability,
            "capability_belief_confidence": self.capability_belief_confidence,
            "believed_competitor_capabilities": self.believed_competitor_capabilities,
            "fundamental_research": self.fundamental_research,
            "training_optimization": self.training_optimization,
            "evaluation_engineering": self.evaluation_engineering,
            "safety_alignment": self.safety_alignment,
            "effort_budget": self.effort_budget,
            "past_strategies": self.past_strategies,
            "observed_competitor_scores": self.observed_competitor_scores,
            "recent_insights": self.recent_insights,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ProviderPrivateState":
        """Create from dict."""
        return cls(**data)

    def get_summary(self) -> str:
        """Get human-readable summary for prompts."""
        summary = f"Strategy Profile: {self.strategy_profile}\n"
        summary += f"Core Traits: {self.innate_traits}\n"
        summary += f"Believed Own Capability: {self.believed_own_capability:.2f}\n"
        summary += f"Believed Benchmark Exploitability: {self.believed_benchmark_exploitability:.2f}\n"
        summary += "Current Investment Portfolio:\n"
        summary += f"  Fundamental Research: {self.fundamental_research:.0%}\n"
        summary += f"  Training Optimization: {self.training_optimization:.0%}\n"
        summary += f"  Evaluation Engineering: {self.evaluation_engineering:.0%}\n"
        summary += f"  Safety & Alignment: {self.safety_alignment:.0%}\n"

        if self.believed_competitor_capabilities:
            summary += "Competitor Capability Beliefs:\n"
            for name, cap in self.believed_competitor_capabilities.items():
                summary += f"  {name}: {cap:.2f}\n"

        return summary

    def get_history_summary(self, n_recent: int = 5) -> str:
        """Get recent strategy history for prompts."""
        summary = "Recent Investment History:\n"
        if self.past_strategies:
            recent = self.past_strategies[-n_recent:]
            summary += "| Round | Research | Training | Eval Eng | Safety |\n"
            summary += "|-------|----------|----------|----------|--------|\n"
            for entry in recent:
                if isinstance(entry, dict):
                    summary += f"| {entry.get('round', '?')} | {entry.get('fundamental_research', 0):.0%} | {entry.get('training_optimization', 0):.0%} | {entry.get('evaluation_engineering', 0):.0%} | {entry.get('safety_alignment', 0):.0%} |\n"
                elif len(entry) >= 5:
                    # Legacy tuple format: (round, research, training, eval_eng, safety)
                    summary += f"| {entry[0]} | {entry[1]:.0%} | {entry[2]:.0%} | {entry[3]:.0%} | {entry[4]:.0%} |\n"
        else:
            summary += "  No history yet.\n"
        return summary


@dataclass
class ConsumerPrivateState:
    """
    Private state for Consumer actors.

    Only accessible to the owning consumer and the logger.
    """
    # Use case preferences
    use_cases: list = field(default_factory=list)  # e.g., ["coding", "writing", "analysis"]
    budget: float = 100.0  # Monthly budget

    # Current subscription
    current_subscription: Optional[str] = None  # Provider name or None

    # Belief state
    believed_model_quality: dict = field(default_factory=dict)  # {provider_name: quality}

    # Experience history
    satisfaction_history: list = field(default_factory=list)  # [(round, provider, satisfaction), ...]
    subscription_history: list = field(default_factory=list)  # [(round, provider), ...]

    def to_dict(self) -> dict:
        """Convert to dict for serialization."""
        return {
            "use_cases": self.use_cases,
            "budget": self.budget,
            "current_subscription": self.current_subscription,
            "believed_model_quality": self.believed_model_quality,
            "satisfaction_history": self.satisfaction_history,
            "subscription_history": self.subscription_history,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ConsumerPrivateState":
        """Create from dict."""
        return cls(**data)

    def get_summary(self) -> str:
        """Get human-readable summary for prompts."""
        summary = f"Use Cases: {', '.join(self.use_cases) if self.use_cases else 'General'}\n"
        summary += f"Budget: ${self.budget:.0f}/month\n"
        summary += f"Current Subscription: {self.current_subscription or 'None'}\n"

        if self.believed_model_quality:
            summary += "Model Quality Beliefs:\n"
            for name, quality in self.believed_model_quality.items():
                summary += f"  {name}: {quality:.2f}\n"

        if self.satisfaction_history:
            recent = self.satisfaction_history[-3:]
            summary += "Recent Experience:\n"
            for round_num, provider, satisfaction in recent:
                summary += f"  Round {round_num} ({provider}): {satisfaction:.2f} satisfaction\n"

        return summary


@dataclass
class PolicymakerPrivateState:
    """
    Private state for Policymaker actors.

    Only accessible to the owning policymaker and the logger.
    """
    # Policy objectives
    policy_objectives: list = field(default_factory=list)  # e.g., ["safety", "fairness", "transparency"]

    # Belief state
    risk_beliefs: dict = field(default_factory=dict)  # {risk_type: belief}
    industry_trust: float = 0.5  # How much policymaker trusts the industry (0-1)

    # Regulatory capacity
    regulatory_capacity: float = 1.0  # Resources available for enforcement

    # History
    past_interventions: list = field(default_factory=list)  # [(round, intervention_type, details), ...]
    observed_incidents: list = field(default_factory=list)  # [(round, incident_description), ...]

    def to_dict(self) -> dict:
        """Convert to dict for serialization."""
        return {
            "policy_objectives": self.policy_objectives,
            "risk_beliefs": self.risk_beliefs,
            "industry_trust": self.industry_trust,
            "regulatory_capacity": self.regulatory_capacity,
            "past_interventions": self.past_interventions,
            "observed_incidents": self.observed_incidents,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PolicymakerPrivateState":
        """Create from dict."""
        return cls(**data)

    def get_summary(self) -> str:
        """Get human-readable summary for prompts."""
        summary = f"Policy Objectives: {', '.join(self.policy_objectives) if self.policy_objectives else 'General oversight'}\n"
        summary += f"Industry Trust Level: {self.industry_trust:.2f}\n"
        summary += f"Regulatory Capacity: {self.regulatory_capacity:.2f}\n"

        if self.risk_beliefs:
            summary += "Risk Assessments:\n"
            for risk, belief in self.risk_beliefs.items():
                summary += f"  {risk}: {belief:.2f}\n"

        if self.past_interventions:
            recent = self.past_interventions[-3:]
            summary += "Recent Interventions:\n"
            for round_num, intervention_type, details in recent:
                summary += f"  Round {round_num}: {intervention_type} - {details}\n"

        return summary


@dataclass
class ProviderGroundTruth:
    """
    Ground truth for Model Provider actors.

    INVISIBLE - Only accessible to simulation and logger.
    This data is NEVER passed to actors or included in LLM prompts.
    """
    true_capability: float = 0.5

    def to_dict(self) -> dict:
        """Convert to dict for serialization."""
        return {"true_capability": self.true_capability}

    @classmethod
    def from_dict(cls, data: dict) -> "ProviderGroundTruth":
        """Create from dict."""
        return cls(**data)


@dataclass
class ConsumerGroundTruth:
    """
    Ground truth for Consumer actors.

    INVISIBLE - Only accessible to simulation and logger.
    """
    # Actual satisfaction based on true model capability vs their needs
    true_satisfaction: float = 0.5
    # Their actual sensitivity to quality differences
    true_quality_sensitivity: float = 0.5

    def to_dict(self) -> dict:
        """Convert to dict for serialization."""
        return {
            "true_satisfaction": self.true_satisfaction,
            "true_quality_sensitivity": self.true_quality_sensitivity,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ConsumerGroundTruth":
        """Create from dict."""
        return cls(**data)


@dataclass
class PolicymakerGroundTruth:
    """
    Ground truth for Policymaker actors.

    INVISIBLE - Only accessible to simulation and logger.
    """
    # Their actual risk tolerance (may differ from stated beliefs)
    true_risk_tolerance: float = 0.5
    # How effective their interventions actually are
    true_intervention_effectiveness: float = 0.5

    def to_dict(self) -> dict:
        """Convert to dict for serialization."""
        return {
            "true_risk_tolerance": self.true_risk_tolerance,
            "true_intervention_effectiveness": self.true_intervention_effectiveness,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PolicymakerGroundTruth":
        """Create from dict."""
        return cls(**data)


# Type aliases for clarity
PrivateState = ProviderPrivateState | ConsumerPrivateState | PolicymakerPrivateState
GroundTruth = ProviderGroundTruth | ConsumerGroundTruth | PolicymakerGroundTruth
