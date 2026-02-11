"""
Media Actor for Evaluation Ecosystem Simulation

Represents a media outlet that observes public events and publishes coverage
that influences consumer beliefs, policymaker risk perception, and funder sentiment.

Key dynamics:
- Media observes public data: leaderboard, benchmark params, regulatory actions
- Detects newsworthy events: leader changes, large score movements, interventions
- Publishes coverage with sentiment and per-provider attention
- Coverage modulates how downstream actors update their beliefs

Designed so multiple instances can coexist in future (different biases/reach).

Visibility:
- PUBLIC: published coverage (headlines, sentiment)
- PRIVATE: editorial_bias, amplification, internal tracking
- INVISIBLE: true_influence, accuracy (held by simulation)
"""
import json
import os
from dataclasses import dataclass, field
from typing import Optional

import numpy as np


@dataclass
class MediaCoverage:
    """Coverage output for a single round."""
    headlines: list = field(default_factory=list)
    sentiment: float = 0.0          # -1 (critical) to +1 (tech-optimistic)
    provider_attention: dict = field(default_factory=dict)  # {provider: 0-1}
    risk_signals: list = field(default_factory=list)
    benchmark_attention: dict = field(default_factory=dict)  # {benchmark: 0-1}

    def to_dict(self) -> dict:
        return {
            "headlines": self.headlines,
            "sentiment": self.sentiment,
            "provider_attention": self.provider_attention,
            "risk_signals": self.risk_signals,
            "benchmark_attention": self.benchmark_attention,
        }


class Media:
    """
    A media outlet that observes public events and publishes coverage.

    Designed so multiple instances can coexist in future (different biases/reach).
    For now, a single instance acts as the aggregate tech press.
    """

    def __init__(
        self,
        name: str = "TechPress",
        editorial_bias: float = 0.0,
        amplification: float = 1.0,
        seed: Optional[int] = None,
    ):
        """
        Initialize a Media outlet.

        Args:
            name: Outlet name
            editorial_bias: -1 (critical) to +1 (tech-optimistic)
            amplification: How much media amplifies signals (1.0 = neutral)
            seed: Random seed
        """
        self.name = name
        self.editorial_bias = editorial_bias
        self.amplification = amplification
        self.rng = np.random.default_rng(seed)
        self.coverage_history: list[dict] = []
        self.memory: list[dict] = []

        # Internal tracking for event detection
        self._previous_leaderboard: list = []
        self._previous_scores: dict = {}
        self._current_coverage: Optional[MediaCoverage] = None
        self._previous_per_benchmark_leaders: dict = {}  # {bm_name: provider_name}
        self._previous_market_shares: dict = {}          # {provider_name: share}

    def observe_and_publish(
        self,
        leaderboard: list,
        benchmark_params: dict,
        policymaker_data: dict,
        new_benchmark: Optional[dict],
        round_num: int,
        funder_data: Optional[dict] = None,
        per_benchmark_scores: Optional[dict] = None,
        consumer_data: Optional[dict] = None,
    ) -> dict:
        """
        Observe public data and publish coverage for this round.

        Args:
            leaderboard: [(provider_name, score), ...] sorted descending
            benchmark_params: {bm_name: {validity, exploitability}}
            policymaker_data: {interventions: [...], ...}
            new_benchmark: Optional dict if a new benchmark was introduced
            round_num: Current round number
            funder_data: Optional funder data from previous round
            per_benchmark_scores: Optional {bm_name: {provider: score}} from current round
            consumer_data: Optional consumer data from previous round

        Returns:
            Coverage dict for downstream actors
        """
        coverage = MediaCoverage()
        provider_names = [name for name, _ in leaderboard]

        # Initialize attention at baseline
        for name in provider_names:
            coverage.provider_attention[name] = 0.1

        events_detected = []

        # --- Detect newsworthy events ---

        # 1. New leaderboard leader
        if self._previous_leaderboard:
            prev_leader = self._previous_leaderboard[0][0] if self._previous_leaderboard else None
            curr_leader = leaderboard[0][0] if leaderboard else None
            if prev_leader and curr_leader and prev_leader != curr_leader:
                events_detected.append(f"{curr_leader} takes the lead from {prev_leader}")
                coverage.provider_attention[curr_leader] = max(
                    coverage.provider_attention.get(curr_leader, 0), 0.8
                )
                coverage.provider_attention[prev_leader] = max(
                    coverage.provider_attention.get(prev_leader, 0), 0.5
                )
                coverage.sentiment += 0.2  # leader changes are exciting

        # 2. Large score jumps (> 0.05) — scores are monotonic so only upward
        current_scores = {name: score for name, score in leaderboard}
        for name, score in current_scores.items():
            prev_score = self._previous_scores.get(name)
            if prev_score is not None:
                delta = score - prev_score
                if delta > 0.05:
                    events_detected.append(f"{name} surges by {delta:.3f}")
                    coverage.provider_attention[name] = max(
                        coverage.provider_attention.get(name, 0), 0.6
                    )
                    coverage.sentiment += 0.1
                    if delta > 0.08:
                        events_detected.append(f"{name} appears to release major model update")
                        coverage.provider_attention[name] = max(
                            coverage.provider_attention.get(name, 0), 0.7
                        )

        # 3. Policymaker interventions
        interventions = policymaker_data.get("interventions", [])
        for intervention in interventions:
            itype = intervention.get("type", "unknown")
            pmaker = intervention.get("policymaker", "Regulator")
            focus = intervention.get("details", {}).get("focus", "AI evaluation practices")
            if itype == "investigation":
                events_detected.append(f"{pmaker} launches investigation into {focus}")
            elif itype == "public_warning":
                events_detected.append(f"{pmaker} issues public warning about AI safety concerns")
            elif itype == "mandate_benchmark":
                events_detected.append(f"{pmaker} mandates new benchmark standards")
            elif itype == "compliance_audit":
                events_detected.append(f"{pmaker} initiates compliance audit on AI providers")
            else:
                events_detected.append(f"Regulatory action: {itype}")
            coverage.risk_signals.append(f"regulatory_{itype}")
            coverage.sentiment -= 0.15  # regulation is sobering

        # 4. New benchmark introduction
        if new_benchmark:
            bm_name = new_benchmark.get("name", "unknown")
            events_detected.append(f"New benchmark introduced: {bm_name}")
            coverage.benchmark_attention[bm_name] = 0.7
            coverage.sentiment += 0.1  # new benchmarks are positive innovation

        # 5. Declining benchmark validity (inferred from score volatility)
        for bm_name, params in benchmark_params.items():
            validity = params.get("validity", 1.0)
            if validity < 0.5:
                events_detected.append(f"Benchmark {bm_name} validity concerns (validity={validity:.2f})")
                coverage.risk_signals.append(f"low_validity_{bm_name}")
                coverage.benchmark_attention[bm_name] = max(
                    coverage.benchmark_attention.get(bm_name, 0), 0.5
                )
                coverage.sentiment -= 0.1

        # 6. Score convergence (everyone scoring similarly)
        if len(leaderboard) >= 2:
            scores = [s for _, s in leaderboard]
            score_range = max(scores) - min(scores)
            if score_range < 0.03:
                events_detected.append("Scores converging — is the benchmark meaningful?")
                coverage.risk_signals.append("score_convergence")
                coverage.sentiment -= 0.05

        # 7. Funding decisions
        if funder_data:
            for funder_name, provider_allocations in funder_data.get("allocations", {}).items():
                if provider_allocations:
                    top_provider = max(provider_allocations, key=provider_allocations.get)
                    top_amount = provider_allocations[top_provider]
                    if top_amount > 0:
                        events_detected.append(f"{top_provider} raises ${top_amount:,.0f} from {funder_name}")
                        coverage.provider_attention[top_provider] = max(
                            coverage.provider_attention.get(top_provider, 0), 0.4)
                        coverage.sentiment += 0.05

        # 8. Per-benchmark leader changes
        if per_benchmark_scores:
            for bm_name, bm_scores in per_benchmark_scores.items():
                if bm_scores:
                    current_leader = max(bm_scores, key=bm_scores.get)
                    prev_leader = self._previous_per_benchmark_leaders.get(bm_name)
                    if prev_leader and prev_leader != current_leader:
                        events_detected.append(f"{current_leader} takes #1 on {bm_name}")
                        coverage.provider_attention[current_leader] = max(
                            coverage.provider_attention.get(current_leader, 0), 0.5)
                        coverage.benchmark_attention[bm_name] = max(
                            coverage.benchmark_attention.get(bm_name, 0), 0.4)
                        coverage.sentiment += 0.1
                    self._previous_per_benchmark_leaders[bm_name] = current_leader

        # 9. Consumer switching / market share shifts
        if consumer_data:
            market_shares = consumer_data.get("market_shares", {})
            for provider, share in market_shares.items():
                prev_share = self._previous_market_shares.get(provider)
                if prev_share is not None:
                    share_delta = share - prev_share
                    if share_delta < -0.03:  # lost >3% market share
                        events_detected.append(
                            f"Consumers are turning away from {provider} (market share {share_delta:+.1%})")
                        coverage.provider_attention[provider] = max(
                            coverage.provider_attention.get(provider, 0), 0.5)
                        coverage.sentiment -= 0.1
                    elif share_delta > 0.03:  # gained >3% market share
                        events_detected.append(
                            f"{provider} sees surge in adoption (market share {share_delta:+.1%})")
                        coverage.provider_attention[provider] = max(
                            coverage.provider_attention.get(provider, 0), 0.4)
                        coverage.sentiment += 0.05
            self._previous_market_shares = dict(market_shares)

        # --- Compose coverage ---
        coverage.headlines = events_detected

        # Apply editorial bias and amplification
        coverage.sentiment = (coverage.sentiment + self.editorial_bias) * self.amplification
        # Clamp sentiment to [-1, 1]
        coverage.sentiment = max(-1.0, min(1.0, coverage.sentiment))

        # Amplify attention
        for name in coverage.provider_attention:
            coverage.provider_attention[name] = min(
                1.0, coverage.provider_attention[name] * self.amplification
            )

        # Store
        self._current_coverage = coverage
        self._previous_leaderboard = list(leaderboard)
        self._previous_scores = current_scores

        coverage_dict = coverage.to_dict()
        self.coverage_history.append({
            "round": round_num,
            **coverage_dict,
        })

        self.memory.append({
            "type": "publish",
            "round": round_num,
            "n_headlines": len(events_detected),
            "sentiment": coverage.sentiment,
            "risk_signals": len(coverage.risk_signals),
        })

        return coverage_dict

    def get_coverage(self) -> Optional[dict]:
        """Return current round's coverage dict, or None if not yet published."""
        if self._current_coverage:
            return self._current_coverage.to_dict()
        return None

    def save(self, folder: str):
        """Save media state to folder."""
        os.makedirs(folder, exist_ok=True)
        data = {
            "name": self.name,
            "editorial_bias": self.editorial_bias,
            "amplification": self.amplification,
            "coverage_history": self.coverage_history,
            "_previous_per_benchmark_leaders": self._previous_per_benchmark_leaders,
            "_previous_market_shares": self._previous_market_shares,
        }
        with open(os.path.join(folder, "media.json"), "w") as f:
            json.dump(data, f, indent=2)

    def __repr__(self):
        return (
            f"Media(name='{self.name}', bias={self.editorial_bias}, "
            f"amplification={self.amplification})"
        )
