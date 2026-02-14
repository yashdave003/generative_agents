"""
Consumer Market for Evaluation Ecosystem Simulation

Models the consumer market as segments rather than individuals.
Each segment = archetype × use_case (e.g., "software_dev_leaderboard_follower").

Key dynamics:
- Segments observe leaderboard rankings weighted by their use-case benchmark preferences
- Switching is tracked as proportions within each segment, not headcounts
- Satisfaction depends on true_capability (ground truth), not benchmark scores
- Gaming creates a perception gap: high weighted score but low true satisfaction
- The gap drives probabilistic switching within each segment

Visibility:
- PUBLIC: market_shares (aggregate), switching_rate
- PRIVATE: per-segment beliefs, satisfaction, provider distribution
- INVISIBLE: true_capability (held by simulation)
"""
import json
import math
import os
from dataclasses import dataclass, field
from typing import Optional

import numpy as np


# ============================================================
#  Use-Case Profiles
# ============================================================

USE_CASE_PROFILES = {
    "software_dev": {
        "label": "Software Developer",
        "benchmark_prefs": {"coding": 0.90, "reasoning": 0.08, "writing": 0.02},
    },
    "content_writer": {
        "label": "Content Writer",
        "benchmark_prefs": {"writing": 0.90, "reasoning": 0.08, "coding": 0.02},
    },
    "legal": {
        "label": "Legal Professional",
        "benchmark_prefs": {"reasoning": 0.75, "writing": 0.20, "safety": 0.05},
    },
    "healthcare": {
        "label": "Healthcare Worker",
        "benchmark_prefs": {"safety": 0.75, "reasoning": 0.20, "writing": 0.05},
    },
    "finance": {
        "label": "Finance Analyst",
        "benchmark_prefs": {"reasoning": 0.70, "safety": 0.25, "coding": 0.05},
    },
    "educator": {
        "label": "Educator",
        "benchmark_prefs": {"writing": 0.50, "reasoning": 0.40, "safety": 0.10},
    },
    "customer_service": {
        "label": "Customer Service",
        "benchmark_prefs": {"writing": 0.85, "reasoning": 0.12, "safety": 0.03},
    },
    "researcher": {
        "label": "Researcher",
        "benchmark_prefs": {"reasoning": 0.50, "coding": 0.45, "writing": 0.05},
    },
    "creative": {
        "label": "Creative Professional",
        "benchmark_prefs": {"writing": 0.85, "reasoning": 0.10, "coding": 0.05},
    },
    "marketing": {
        "label": "Marketing Professional",
        "benchmark_prefs": {"writing": 0.75, "reasoning": 0.20, "coding": 0.05},
    },
    "service_worker": {
        "label": "Service Worker",
        "benchmark_prefs": {"writing": 0.65, "reasoning": 0.25, "safety": 0.10},
    },
}


# ============================================================
#  Archetype Definitions
# ============================================================

ARCHETYPES = {
    "leaderboard_follower": {
        "leaderboard_trust": 0.85,
        "switching_cost": 0.05,
        "switching_threshold": 0.15,
    },
    "experience_driven": {
        "leaderboard_trust": 0.35,
        "switching_cost": 0.08,
        "switching_threshold": 0.08,
    },
    "cautious": {
        "leaderboard_trust": 0.50,
        "switching_cost": 0.20,
        "switching_threshold": 0.25,
    },
}


# ============================================================
#  MarketSegment
# ============================================================

@dataclass
class MarketSegment:
    """A segment of the consumer market defined by archetype × use_case."""

    name: str                          # e.g., "software_dev_leaderboard_follower"
    archetype: str                     # "leaderboard_follower" | "experience_driven" | "cautious"
    use_case: str                      # "software_dev" | "healthcare" | etc.
    market_fraction: float             # proportion of total market (sums to 1.0)

    # Resolved benchmark weights {benchmark_name: weight}
    benchmark_weights: dict = field(default_factory=dict)

    # Archetype parameters
    leaderboard_trust: float = 0.7
    switching_cost: float = 0.1
    switching_threshold: float = 0.15

    # Dynamic state
    provider_shares: dict = field(default_factory=dict)    # {provider: proportion}
    believed_quality: dict = field(default_factory=dict)   # {provider: quality_estimate}
    satisfaction: dict = field(default_factory=dict)        # {provider: satisfaction_level}
    tenure: dict = field(default_factory=dict)              # {provider: rounds_subscribed}

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "archetype": self.archetype,
            "use_case": self.use_case,
            "market_fraction": self.market_fraction,
            "benchmark_weights": self.benchmark_weights,
            "leaderboard_trust": self.leaderboard_trust,
            "switching_cost": self.switching_cost,
            "switching_threshold": self.switching_threshold,
            "provider_shares": self.provider_shares,
            "believed_quality": self.believed_quality,
            "satisfaction": self.satisfaction,
            "tenure": self.tenure,
        }


# ============================================================
#  ConsumerMarket
# ============================================================

class ConsumerMarket:
    """
    Manages the entire consumer market as segments.

    Each segment is defined by archetype × use_case, has a fraction of the
    total market, and tracks provider distribution as proportions.

    Replaces individual Consumer objects with aggregate market dynamics.
    """

    def __init__(
        self,
        segments: list[MarketSegment],
        provider_names: list[str],
        brand_recognition: Optional[dict] = None,
        seed: Optional[int] = None,
    ):
        self.segments = segments
        self.provider_names = provider_names
        self.brand_recognition = brand_recognition or {}
        self.rng = np.random.default_rng(seed)
        self.current_round = 0
        self.memory = []
        self._last_segment_switching = {}  # Track per-segment switching rates

        # Initialize provider shares if not already set
        for seg in self.segments:
            if not seg.provider_shares:
                seg.provider_shares = self._initial_shares(provider_names)
            if not seg.tenure:
                seg.tenure = {p: 0 for p in provider_names}

    def _initial_shares(self, provider_names: list[str]) -> dict:
        """Distribute initial market shares weighted by brand recognition."""
        weights = []
        for name in provider_names:
            br = self.brand_recognition.get(name, 0.5)
            weights.append(br)
        total = sum(weights)
        if total == 0:
            return {name: 1.0 / len(provider_names) for name in provider_names}
        return {name: w / total for name, w in zip(provider_names, weights)}

    def resolve_benchmark_weights(self, benchmark_names: list[str]):
        """Map use-case preference categories to actual benchmark names.

        Uses substring matching: "coding_bench" matches category "coding".
        Unmatched benchmarks get a small default weight (0.1).
        """
        for seg in self.segments:
            profile = USE_CASE_PROFILES.get(seg.use_case, {})
            prefs = profile.get("benchmark_prefs", {})
            weights = {}
            for bm_name in benchmark_names:
                matched = False
                for category, pref_weight in prefs.items():
                    if category.lower() in bm_name.lower():
                        weights[bm_name] = pref_weight
                        matched = True
                        break
                if not matched:
                    weights[bm_name] = 0.1  # small default weight
            # Normalize
            total = sum(weights.values())
            if total > 0:
                weights = {k: v / total for k, v in weights.items()}
            seg.benchmark_weights = weights

    def observe(self, leaderboard: list, media_coverage: Optional[dict],
                round_num: int):
        """Update all segments' beliefs from leaderboard.

        Args:
            leaderboard: [(provider_name, score), ...] sorted descending
            media_coverage: Optional media coverage dict (for Phase 5)
            round_num: Current round number
        """
        self.current_round = round_num

        for seg in self.segments:
            learning_rate = 0.3

            # Media modulation (Phase 5 hook — no-op if media_coverage is None)
            if media_coverage:
                sentiment = media_coverage.get("sentiment", 0.0)
                # Positive sentiment → faster adoption of leaderboard signals
                learning_rate = 0.3 * (1 + 0.3 * sentiment)
                learning_rate = max(0.1, min(0.5, learning_rate))

                # Risk signals reduce leaderboard trust for followers
                if (media_coverage.get("risk_signals") and
                        seg.archetype == "leaderboard_follower"):
                    # Temporarily reduce trust (doesn't permanently change archetype)
                    pass  # Will be implemented in Phase 5

            for provider_name, composite_score in leaderboard:
                # Compute use-case-weighted perceived score from per-benchmark
                # scores if available. Falls back to composite score.
                perceived_score = composite_score

                if provider_name not in seg.believed_quality:
                    seg.believed_quality[provider_name] = perceived_score
                else:
                    old = seg.believed_quality[provider_name]
                    seg.believed_quality[provider_name] = (
                        (1 - learning_rate) * old + learning_rate * perceived_score
                    )

    def observe_per_benchmark(self, leaderboard: list,
                              per_benchmark_scores: dict,
                              media_coverage: Optional[dict],
                              round_num: int):
        """Update beliefs using per-benchmark scores weighted by use case.

        When per-benchmark scores are available, each segment weights them
        according to their benchmark_weights for a use-case-specific perception.

        Args:
            leaderboard: [(provider_name, score)] for provider name ordering
            per_benchmark_scores: {benchmark_name: {provider_name: score}}
            media_coverage: Optional media coverage dict
            round_num: Current round number
        """
        self.current_round = round_num

        for seg in self.segments:
            learning_rate = 0.3

            if media_coverage:
                sentiment = media_coverage.get("sentiment", 0.0)
                learning_rate = 0.3 * (1 + 0.3 * sentiment)
                learning_rate = max(0.1, min(0.5, learning_rate))

            for provider_name, _ in leaderboard:
                # Compute weighted score based on segment's benchmark preferences
                weighted_score = 0.0
                total_weight = 0.0
                for bm_name, bm_weight in seg.benchmark_weights.items():
                    bm_scores = per_benchmark_scores.get(bm_name, {})
                    if provider_name in bm_scores:
                        weighted_score += bm_weight * bm_scores[provider_name]
                        total_weight += bm_weight
                if total_weight > 0:
                    perceived_score = weighted_score / total_weight
                else:
                    # Fallback to composite
                    perceived_score = next(
                        (s for n, s in leaderboard if n == provider_name), 0.5
                    )

                if provider_name not in seg.believed_quality:
                    seg.believed_quality[provider_name] = perceived_score
                else:
                    old = seg.believed_quality[provider_name]
                    seg.believed_quality[provider_name] = (
                        (1 - learning_rate) * old + learning_rate * perceived_score
                    )

    def compute_satisfaction(
        self,
        ground_truth: dict,
        provider_strategies: Optional[dict] = None,
        published_scores: Optional[dict] = None,
        media_coverage: Optional[dict] = None,
    ):
        """Compute per-segment per-provider satisfaction from ground truth.

        Satisfaction is now primarily based on believed_quality (use-case weighted
        perceived performance), adjusted for:
        1. Gaming detection penalty (score inflation above true capability)
        2. Safety alignment match (provider safety investment × segment safety preference)
        3. Media sentiment influence (negative coverage reduces satisfaction)

        This creates natural differentiation across use cases: software developers
        experience satisfaction based on coding performance, healthcare workers based
        on safety/reasoning performance, etc.

        Args:
            ground_truth: {provider_name: ProviderGroundTruth}
            provider_strategies: {provider_name: {fundamental_research, ...}}
            published_scores: {provider_name: composite_score}
            media_coverage: Media coverage dict with sentiment and provider_attention
        """
        for seg in self.segments:
            for provider_name in self.provider_names:
                if provider_name not in ground_truth:
                    continue

                gt = ground_truth[provider_name]
                true_capability = gt.true_capability

                # Base satisfaction: use-case weighted perceived quality
                # This is what the segment actually experiences in their domain
                base_satisfaction = seg.believed_quality.get(provider_name, true_capability)

                # If no believed_quality yet (early rounds), use true_capability
                if provider_name not in seg.believed_quality:
                    base_satisfaction = true_capability

                # Factor 1: Gaming Detection Penalty
                # If score >> true_capability, consumer experiences disappointment
                # (high scores attracted them, but actual performance disappoints)
                gaming_penalty = 0.0
                if published_scores and provider_name in published_scores:
                    score = published_scores[provider_name]
                    gap = max(0, score - true_capability)
                    gaming_penalty = 0.20 * gap  # 20% penalty per unit of inflation

                # Factor 2: Safety Alignment Match
                # Segments with high safety preferences value safety investment
                safety_bonus = 0.0
                if provider_strategies and provider_name in provider_strategies:
                    strategy = provider_strategies[provider_name]
                    safety_investment = strategy.get("safety_alignment", 0.0)
                    # Get segment's safety preference weight
                    safety_pref = 0.0
                    for cat, weight in USE_CASE_PROFILES.get(seg.use_case, {}).get("benchmark_prefs", {}).items():
                        if "safety" in cat.lower():
                            safety_pref = weight
                            break
                    # Bonus scales with both provider investment and segment preference
                    safety_bonus = 0.12 * safety_investment * safety_pref

                # Factor 3: Media Sentiment Influence
                # Negative media coverage reduces satisfaction beyond objective metrics
                media_penalty = 0.0
                if media_coverage:
                    sentiment = media_coverage.get("sentiment", 0.0)
                    provider_attention = media_coverage.get("provider_attention", {}).get(provider_name, 0.0)
                    # Only negative sentiment creates penalty
                    if sentiment < 0:
                        media_penalty = 0.10 * abs(sentiment) * provider_attention

                # Compute final satisfaction
                satisfaction = (
                    base_satisfaction
                    - gaming_penalty
                    + safety_bonus
                    - media_penalty
                )

                # Clamp to [0, 1]
                seg.satisfaction[provider_name] = max(0.0, min(1.0, satisfaction))

    def compute_switching(self):
        """Compute switching proportions within each segment.

        Two triggers (same logic as original Consumer, but applied proportionally):
        1. Dissatisfaction: believed quality > actual satisfaction by > threshold
        2. Opportunity: a better alternative exceeds switching cost + tenure bonus

        Returns:
            Total switching rate (fraction of total market that switched)
        """
        total_switching = 0.0

        # Track per-segment switching for analysis
        segment_switching_rates = {}

        for seg in self.segments:
            seg_switching = 0.0

            for provider in list(seg.provider_shares.keys()):
                share = seg.provider_shares.get(provider, 0.0)
                if share < 0.001:  # skip negligible shares
                    continue

                tenure_bonus = min(0.1, seg.tenure.get(provider, 0) * 0.02)
                should_switch_prob = 0.0
                best_alternative = None
                best_alt_score = -1.0

                # --- Trigger 1: Dissatisfaction ---
                believed = seg.believed_quality.get(provider, 0.5)
                actual_sat = seg.satisfaction.get(provider, 0.5)
                gap = believed - actual_sat

                threshold = seg.switching_threshold + tenure_bonus + seg.switching_cost
                if gap > 0:
                    # Sigmoid-based probability: smooth transition
                    should_switch_prob = max(
                        should_switch_prob,
                        _switching_probability(gap, threshold),
                    )

                # --- Trigger 2: Better alternative ---
                current_blended = self._blended_score(seg, provider)
                opportunity_threshold = seg.switching_cost + tenure_bonus

                for alt_provider in self.provider_names:
                    if alt_provider == provider:
                        continue
                    alt_blended = self._blended_score(seg, alt_provider)
                    improvement = alt_blended - current_blended
                    if improvement > 0:
                        opp_prob = _switching_probability(
                            improvement, opportunity_threshold
                        )
                        if opp_prob > should_switch_prob:
                            should_switch_prob = opp_prob
                        if alt_blended > best_alt_score:
                            best_alt_score = alt_blended
                            best_alternative = alt_provider

                # Apply switching
                if should_switch_prob > 0.01 and best_alternative:
                    switching_fraction = should_switch_prob * share
                    switching_fraction = min(switching_fraction, share)  # can't exceed current share

                    seg.provider_shares[provider] -= switching_fraction
                    seg.provider_shares[best_alternative] = (
                        seg.provider_shares.get(best_alternative, 0.0) + switching_fraction
                    )
                    seg_switching += switching_fraction

                    # Reset tenure for switchers
                    seg.tenure[provider] = max(0, seg.tenure.get(provider, 0) - 1)

            # Update tenure for remaining subscribers
            for provider in self.provider_names:
                if seg.provider_shares.get(provider, 0) > 0.01:
                    seg.tenure[provider] = seg.tenure.get(provider, 0) + 1

            # Normalize shares to prevent drift
            total_share = sum(seg.provider_shares.values())
            if total_share > 0:
                seg.provider_shares = {
                    k: v / total_share for k, v in seg.provider_shares.items()
                }

            total_switching += seg_switching * seg.market_fraction

            # Store per-segment switching rate
            segment_switching_rates[seg.name] = seg_switching

        # Store for later retrieval
        self._last_segment_switching = segment_switching_rates

        return total_switching

    def _blended_score(self, seg: MarketSegment, provider: str) -> float:
        """Compute blended perceived quality for a provider within a segment."""
        trust = seg.leaderboard_trust
        believed = seg.believed_quality.get(provider, 0.5)
        actual_sat = seg.satisfaction.get(provider, 0.5)
        # Blend leaderboard-derived belief with actual experience
        return trust * believed + (1 - trust) * actual_sat

    def get_consumer_data(self) -> dict:
        """Return consumer_data dict compatible with downstream systems.

        Returns dict with:
            market_shares: {provider: proportion} aggregated across segments
            provider_satisfaction: {provider: avg_satisfaction} weighted by share
            avg_satisfaction: float — market-wide weighted average
            switching_rate: float — stored from last compute_switching()
            segment_data: {segment_name: {provider_shares, satisfaction}}
        """
        # Aggregate market shares across segments
        market_shares = {p: 0.0 for p in self.provider_names}
        for seg in self.segments:
            for provider, share in seg.provider_shares.items():
                market_shares[provider] = (
                    market_shares.get(provider, 0.0) + share * seg.market_fraction
                )

        # Per-provider satisfaction (weighted by market share across segments)
        provider_satisfaction = {}
        for provider in self.provider_names:
            weighted_sat = 0.0
            total_weight = 0.0
            for seg in self.segments:
                seg_share = seg.provider_shares.get(provider, 0.0)
                weight = seg_share * seg.market_fraction
                if weight > 0:
                    sat = seg.satisfaction.get(provider, 0.5)
                    weighted_sat += sat * weight
                    total_weight += weight
            if total_weight > 0:
                provider_satisfaction[provider] = weighted_sat / total_weight
            else:
                provider_satisfaction[provider] = 0.0

        # Market-wide average satisfaction
        avg_satisfaction = 0.0
        total_share = sum(market_shares.values())
        if total_share > 0:
            for provider, share in market_shares.items():
                avg_satisfaction += (
                    provider_satisfaction.get(provider, 0.0) * share
                )
            avg_satisfaction /= total_share

        # Segment data for detailed analysis
        segment_data = {}
        for seg in self.segments:
            segment_data[seg.name] = {
                "archetype": seg.archetype,
                "use_case": seg.use_case,
                "market_fraction": seg.market_fraction,
                "provider_shares": dict(seg.provider_shares),
                "satisfaction": dict(seg.satisfaction),
                "switching_rate": self._last_segment_switching.get(seg.name, 0.0),
            }

        return {
            "market_shares": market_shares,
            "provider_satisfaction": provider_satisfaction,
            "avg_satisfaction": avg_satisfaction,
            "switching_rate": 0.0,  # set by caller after compute_switching()
            "segment_data": segment_data,
        }

    def save(self, folder: str):
        """Save consumer market state to folder."""
        os.makedirs(folder, exist_ok=True)
        data = {
            "provider_names": self.provider_names,
            "brand_recognition": self.brand_recognition,
            "current_round": self.current_round,
            "segments": [seg.to_dict() for seg in self.segments],
        }
        with open(os.path.join(folder, "consumer_market.json"), "w") as f:
            json.dump(data, f, indent=2)

    def __repr__(self):
        return (
            f"ConsumerMarket(segments={len(self.segments)}, "
            f"providers={self.provider_names})"
        )


# ============================================================
#  Helper Functions
# ============================================================

def _switching_probability(gap: float, threshold: float,
                           steepness: float = 10.0) -> float:
    """Sigmoid-based switching probability.

    Args:
        gap: The dissatisfaction or improvement gap
        threshold: The switching threshold
        steepness: How sharp the sigmoid transition is (default 10)

    Returns:
        Probability of switching (0-1)
    """
    x = steepness * (gap - threshold)
    # Clamp to avoid overflow
    x = max(-20.0, min(20.0, x))
    return 1.0 / (1.0 + math.exp(-x))


def create_default_segments(
    use_cases: list[str],
    provider_names: list[str],
    brand_recognition: Optional[dict] = None,
    archetype_weights: Optional[dict] = None,
) -> list[MarketSegment]:
    """Create market segments from use cases and archetypes.

    Args:
        use_cases: List of use case profile keys (e.g., ["software_dev", "healthcare"])
        provider_names: List of provider names
        brand_recognition: Optional {provider: recognition_factor}
        archetype_weights: Optional custom archetype distribution.
            Default: {"leaderboard_follower": 0.4, "experience_driven": 0.35, "cautious": 0.25}

    Returns:
        List of MarketSegment objects with equal market fractions per use case
    """
    if archetype_weights is None:
        archetype_weights = {
            "leaderboard_follower": 0.40,
            "experience_driven": 0.35,
            "cautious": 0.25,
        }

    segments = []
    n_use_cases = len(use_cases)

    for use_case in use_cases:
        profile = USE_CASE_PROFILES.get(use_case)
        if profile is None:
            continue

        use_case_fraction = 1.0 / n_use_cases

        for archetype, arch_weight in archetype_weights.items():
            arch_params = ARCHETYPES.get(archetype, ARCHETYPES["cautious"])
            seg_fraction = use_case_fraction * arch_weight

            # Initial provider shares from brand recognition
            shares = {}
            if brand_recognition:
                weights = [brand_recognition.get(p, 0.5) for p in provider_names]
                total = sum(weights)
                shares = {p: w / total for p, w in zip(provider_names, weights)}
            else:
                shares = {p: 1.0 / len(provider_names) for p in provider_names}

            seg = MarketSegment(
                name=f"{use_case}_{archetype}",
                archetype=archetype,
                use_case=use_case,
                market_fraction=seg_fraction,
                leaderboard_trust=arch_params["leaderboard_trust"],
                switching_cost=arch_params["switching_cost"],
                switching_threshold=arch_params["switching_threshold"],
                provider_shares=shares,
                believed_quality={},
                satisfaction={},
                tenure={p: 0 for p in provider_names},
            )
            segments.append(seg)

    return segments


# ============================================================
#  Deprecated: Individual Consumer (kept for loading old experiments)
# ============================================================

class Consumer:
    """DEPRECATED: Individual consumer model. Kept for loading old experiments.

    New code should use ConsumerMarket + MarketSegment instead.
    """

    def __init__(self, name, use_cases=None, budget=100.0,
                 quality_sensitivity=0.5, switching_threshold=0.3,
                 leaderboard_trust=0.7, switching_cost=0.1, llm_mode=False):
        from visibility import PublicState, ConsumerPrivateState
        self.public_state = PublicState(name=name, current_round=0, published_scores=[])
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
        self.quality_sensitivity = quality_sensitivity
        self.switching_threshold = switching_threshold
        self.llm_mode = llm_mode
        self.memory = []
        self._last_leaderboard = []
        self._brand_recognition = {}

    @property
    def name(self):
        return self.public_state.name

    def observe(self, leaderboard, round_num):
        self.public_state.current_round = round_num
        self._last_leaderboard = leaderboard
        for provider_name, score in leaderboard:
            if provider_name not in self.private_state.believed_model_quality:
                self.private_state.believed_model_quality[provider_name] = score
            else:
                lr = 0.3
                old = self.private_state.believed_model_quality[provider_name]
                self.private_state.believed_model_quality[provider_name] = (1 - lr) * old + lr * score
        self.memory.append({"type": "observation", "round": round_num, "leaderboard": leaderboard})

    def reflect(self):
        if not self.private_state.satisfaction_history:
            return
        recent = self.private_state.satisfaction_history[-3:]
        current_sub = self.private_state.current_subscription
        if not current_sub:
            return
        recent_with_current = [sat for _, provider, sat in recent if provider == current_sub]
        if recent_with_current:
            avg_sat = sum(recent_with_current) / len(recent_with_current)
            expected = self.private_state.believed_model_quality.get(current_sub, 0.5)
            self.private_state.believed_model_quality[current_sub] = 0.6 * expected + 0.4 * avg_sat

    def plan(self):
        return self._plan_heuristic()

    def _plan_heuristic(self):
        current_sub = self.private_state.current_subscription
        should_switch = False
        switch_reason = ""
        if current_sub and self._last_leaderboard:
            tenure_bonus = min(0.1, self.private_state.rounds_with_provider * 0.02)
            if self.private_state.satisfaction_history:
                recent = [sat for _, provider, sat in self.private_state.satisfaction_history[-3:]
                          if provider == current_sub]
                if recent:
                    avg_sat = sum(recent) / len(recent)
                    lb_exp = next((s for n, s in self._last_leaderboard if n == current_sub), None)
                    if lb_exp is None:
                        lb_exp = self.private_state.believed_model_quality.get(current_sub, 0.5)
                    gap = lb_exp - avg_sat
                    threshold = self.switching_threshold + tenure_bonus + self.private_state.switching_cost
                    if gap > threshold:
                        should_switch = True
                        switch_reason = f"dissatisfied: gap={gap:.3f} > threshold={threshold:.3f}"
            if not should_switch:
                current_lb = next((s for n, s in self._last_leaderboard if n == current_sub), None)
                if current_lb is not None:
                    trust = self.private_state.leaderboard_trust
                    br = self._brand_recognition.get(current_sub, 0.5)
                    cur_believed = self.private_state.believed_model_quality.get(current_sub, current_lb * br)
                    cur_blended = trust * current_lb + (1 - trust) * cur_believed
                    opp_threshold = self.private_state.switching_cost + tenure_bonus
                    for name, score in self._last_leaderboard:
                        if name == current_sub:
                            continue
                        alt_br = self._brand_recognition.get(name, 0.5)
                        alt_believed = self.private_state.believed_model_quality.get(name, score * alt_br)
                        alt_blended = trust * score + (1 - trust) * alt_believed
                        if alt_blended - cur_blended > opp_threshold:
                            should_switch = True
                            switch_reason = f"better option: {name}"
                            break
        if should_switch or current_sub is None:
            if not self._last_leaderboard:
                return None
            best_score = -1
            best = None
            for pn, lbs in self._last_leaderboard:
                trust = self.private_state.leaderboard_trust
                br = self._brand_recognition.get(pn, 0.5)
                believed = self.private_state.believed_model_quality.get(pn, lbs * br)
                blended = trust * lbs + (1 - trust) * believed
                if blended > best_score:
                    best_score = blended
                    best = pn
            self.memory.append({"type": "planning", "round": self.public_state.current_round,
                                "decision": "switch" if current_sub else "subscribe",
                                "provider": best, "from": current_sub, "reason": switch_reason or "initial"})
            return best
        self.memory.append({"type": "planning", "round": self.public_state.current_round,
                            "decision": "stay", "provider": current_sub, "reason": "satisfied"})
        return current_sub

    def execute(self, new_subscription=None):
        if new_subscription is None:
            new_subscription = self.plan()
        old_sub = self.private_state.current_subscription
        if old_sub != new_subscription:
            self.memory.append({"type": "subscription_change", "round": self.public_state.current_round,
                                "from": old_sub, "to": new_subscription})
        self.private_state.current_subscription = new_subscription
        if new_subscription:
            self.private_state.subscription_history.append((self.public_state.current_round, new_subscription))

    def receive_satisfaction(self, satisfaction):
        current_sub = self.private_state.current_subscription
        if current_sub:
            self.private_state.satisfaction_history.append(
                (self.public_state.current_round, current_sub, satisfaction))

    def save(self, folder):
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, "public_state.json"), "w") as f:
            json.dump(self.public_state.to_dict(), f, indent=2)
        with open(os.path.join(folder, "private_state.json"), "w") as f:
            json.dump(self.private_state.to_dict(), f, indent=2)
        with open(os.path.join(folder, "memory.json"), "w") as f:
            json.dump(self.memory, f, indent=2)

    def __repr__(self):
        return f"Consumer(name='{self.name}', subscription='{self.private_state.current_subscription}')"
