"""
Evaluator Actor for Evaluation Ecosystem Simulation

Represents an organization that designs and operates benchmarks.
The Evaluator determines benchmark properties and scores models.

Key visibility design:
- The evaluator receives ground truth from the simulation, not from actors
- This ensures actors cannot leak invisible information to each other
"""
import json
import numpy as np
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from visibility import ProviderGroundTruth


@dataclass
class Benchmark:
    """
    Represents a benchmark with properties that determine scoring behavior.

    The scoring model with investment portfolio:
        score ~ Normal(true_capability + eval_engineering × exploitability, (σ/√α)²)

    Where:
    - α (validity): Measurement precision — higher = lower noise (0-1)
    - exploitability: How much evaluation engineering inflates scores (0-1)
    - eval_engineering: Provider's investment in benchmark-specific optimization
    - σ (noise_level): Base noise standard deviation
    - Gaming (eval_eng × exploitability) inflates scores ABOVE true capability
    - Validity controls noise magnitude, not signal scaling
    """
    name: str = "default_benchmark"

    # Measurement precision (0-1)
    # Higher = less noise, benchmark more reliably measures true capability
    # Lower = noisier scores, less discriminating between providers
    validity: float = 0.7

    # How much evaluation engineering affects scores (0-1)
    # Higher = easier to inflate scores through benchmark optimization
    exploitability: float = 0.5

    # Base standard deviation of score noise (scaled by 1/√validity)
    noise_level: float = 0.1

    # Optional: decay of validity over time as providers adapt
    validity_decay_rate: float = 0.0

    # Optional: how much exploitability increases as providers learn to optimize
    exploitability_growth_rate: float = 0.0

    def get_summary(self) -> str:
        """Return a human-readable summary of benchmark properties."""
        return (
            f"Benchmark: {self.name}\n"
            f"  Validity (alpha): {self.validity:.2f}\n"
            f"  Exploitability (beta): {self.exploitability:.2f}\n"
            f"  Noise (sigma): {self.noise_level:.2f}"
        )


@dataclass
class Regulation:
    """
    Represents a regulatory requirement that affects evaluation.

    Regulations can be issued by Policymakers to change benchmark behavior.
    """
    name: str = ""
    regulation_type: str = ""  # "mandate_benchmark", "set_threshold", "require_disclosure"
    details: dict = field(default_factory=dict)
    issued_round: int = 0
    active: bool = True

    def get_summary(self) -> str:
        """Return a human-readable summary of the regulation."""
        status = "Active" if self.active else "Inactive"
        return f"{self.name} ({self.regulation_type}): {status} - {self.details}"


class Evaluator:
    """
    An Evaluator agent in the evaluation ecosystem simulation.

    The Evaluator:
    - Maintains one or more benchmarks with different properties
    - Scores models based on their true capability and evaluation engineering
    - Publishes scores that providers observe

    Key visibility design:
    - Ground truth (true_capability) is passed FROM the simulation
    - The evaluator does NOT access actor.true_capability directly
    - This enforces the visibility boundary: actors can't see each other's ground truth

    Multi-benchmark support:
    - Can hold multiple benchmarks with different validity/exploitability
    - Providers are scored on all benchmarks
    - Composite score can be computed as weighted average

    Scoring model:
        score ~ Normal(true_capability + eval_engineering × exploitability, (σ/√α)²)
    Gaming inflates scores above true capability. Validity controls noise precision.
    """

    def __init__(
        self,
        benchmark_name: str = "default_benchmark",
        validity: float = 0.7,
        exploitability: float = 0.5,
        noise_level: float = 0.1,
        seed: Optional[int] = None,
        benchmarks: Optional[list[dict]] = None,
    ):
        """
        Initialize an Evaluator.

        Args:
            benchmark_name: Name of the primary benchmark (ignored if benchmarks provided)
            validity: α - measurement precision, controls noise (0-1)
            exploitability: how much eval engineering inflates scores (0-1)
            noise_level: σ - base standard deviation of score noise
            seed: Random seed for reproducibility
            benchmarks: Optional list of benchmark configs for multi-benchmark mode.
                       Each dict should have: name, validity, exploitability, noise_level, weight
        """
        # Support for multiple benchmarks
        self.benchmarks: list[Benchmark] = []
        self.benchmark_weights: dict[str, float] = {}

        if benchmarks:
            # Multi-benchmark mode
            for bm_config in benchmarks:
                bm = Benchmark(
                    name=bm_config.get("name", f"benchmark_{len(self.benchmarks)}"),
                    validity=bm_config.get("validity", 0.7),
                    exploitability=bm_config.get("exploitability", 0.5),
                    noise_level=bm_config.get("noise_level", 0.1),
                )
                self.benchmarks.append(bm)
                self.benchmark_weights[bm.name] = bm_config.get("weight", 1.0)
        else:
            # Single benchmark mode (backwards compatible)
            self.benchmarks.append(Benchmark(
                name=benchmark_name,
                validity=validity,
                exploitability=exploitability,
                noise_level=noise_level,
            ))
            self.benchmark_weights[benchmark_name] = 1.0

        # Primary benchmark reference (backwards compatibility)
        self.benchmark = self.benchmarks[0]

        # Random state for reproducibility
        self.rng = np.random.default_rng(seed)

        # History of published scores
        # Format: [(round, {provider_name: score}), ...]
        # For multi-benchmark: [(round, {provider_name: {benchmark_name: score, "composite": score}}), ...]
        self.score_history: list = []

        # Per-benchmark score history
        # Format: {benchmark_name: [(round, {provider_name: score}), ...]}
        self.benchmark_score_history: dict[str, list] = {bm.name: [] for bm in self.benchmarks}

        # History of true capabilities (for analysis, not visible to providers)
        # Format: [(round, {provider_name: true_capability}), ...]
        self.capability_history: list = []

        # Current round
        self.current_round: int = 0

        # Active regulations (from policymakers)
        self.active_regulations: list[Regulation] = []

        # Benchmark introduction parameters
        self.benchmark_introduction_cooldown: int = 7
        self.last_introduction_round: int = 0  # first introduction at round 8
        self.max_benchmarks: int = 6
        self.introduction_history: list[dict] = []  # [{round, benchmark_name, trigger}]

        # Per-benchmark best published scores (monotonicity enforcement)
        self._best_published_scores: dict[str, dict[str, float]] = {
            bm.name: {} for bm in self.benchmarks
        }

    def evaluate(
        self,
        true_capability: float,
        evaluation_engineering: float,
        benchmark: Optional[Benchmark] = None,
    ) -> float:
        """
        Generate a benchmark score for a model on a specific benchmark.

        The scoring model:
            score ~ Normal(true_capability + eval_engineering × exploitability, (σ/√α)²)

        Gaming (eval_engineering × exploitability) inflates scores above true capability.
        Validity (α) controls noise — lower validity = noisier, less discriminating scores.

        Args:
            true_capability: The model's actual capability level (from ground truth)
            evaluation_engineering: How much the provider invested in benchmark-specific optimization
            benchmark: Specific benchmark to use (defaults to primary benchmark)

        Returns:
            The observed benchmark score (stochastic)
        """
        if benchmark is None:
            benchmark = self.benchmark

        # Expected score: true capability + gaming inflation
        mean_score = true_capability + evaluation_engineering * benchmark.exploitability

        # Noise scaled by validity: lower validity = more noise
        noise_std = benchmark.noise_level / np.sqrt(max(benchmark.validity, 0.05))
        score = self.rng.normal(mean_score, noise_std)

        # Clamp to [0, 1] range
        score = max(0.0, min(1.0, score))

        return score

    def evaluate_on_benchmark(
        self,
        true_capability: float,
        evaluation_engineering: float,
        benchmark_name: str,
    ) -> float:
        """
        Evaluate on a specific benchmark by name.

        Args:
            true_capability: The model's actual capability level
            evaluation_engineering: Investment in benchmark optimization
            benchmark_name: Name of benchmark to evaluate on

        Returns:
            The benchmark score
        """
        benchmark = next((b for b in self.benchmarks if b.name == benchmark_name), None)
        if benchmark is None:
            raise ValueError(f"Unknown benchmark: {benchmark_name}")
        return self.evaluate(true_capability, evaluation_engineering, benchmark)

    def evaluate_all(
        self,
        providers: list,
        round_num: int,
        ground_truth: Optional[dict] = None,
    ) -> dict:
        """
        Evaluate all providers on all benchmarks and return composite scores.

        For single benchmark: returns {provider_name: score}
        For multiple benchmarks: returns {provider_name: composite_score}
        Also stores per-benchmark scores in benchmark_score_history.

        Args:
            providers: List of ModelProvider objects
            round_num: Current simulation round
            ground_truth: Dict mapping provider names to ProviderGroundTruth objects
                         If None, falls back to provider.true_capability for backwards compatibility

        Returns:
            Dict mapping provider names to composite scores
        """
        self.current_round = round_num
        composite_scores = {}
        capabilities = {}
        per_benchmark_scores = {bm.name: {} for bm in self.benchmarks}

        for provider in providers:
            # Get true capability from ground truth dict if provided
            if ground_truth is not None and provider.name in ground_truth:
                true_cap = ground_truth[provider.name].true_capability
            else:
                # Backwards compatibility: access from provider
                true_cap = provider.true_capability

            capabilities[provider.name] = true_cap

            # Evaluate on each benchmark
            weighted_sum = 0.0
            total_weight = 0.0

            for benchmark in self.benchmarks:
                score = self.evaluate(
                    true_capability=true_cap,
                    evaluation_engineering=provider.evaluation_engineering,
                    benchmark=benchmark,
                )

                # Monotonicity: providers wouldn't disclose a worse score
                best = self._best_published_scores[benchmark.name].get(provider.name, 0.0)
                score = max(score, best)
                self._best_published_scores[benchmark.name][provider.name] = score

                per_benchmark_scores[benchmark.name][provider.name] = score

                weight = self.benchmark_weights.get(benchmark.name, 1.0)
                weighted_sum += score * weight
                total_weight += weight

            # Compute composite score (weighted average)
            composite_scores[provider.name] = weighted_sum / total_weight if total_weight > 0 else 0.0

        # Record per-benchmark history
        for bm_name, scores in per_benchmark_scores.items():
            self.benchmark_score_history[bm_name].append((round_num, dict(scores)))

        # Record composite history (backwards compatible)
        self.score_history.append((round_num, dict(composite_scores)))
        self.capability_history.append((round_num, dict(capabilities)))

        return composite_scores

    def get_per_benchmark_scores(self, round_num: int) -> dict:
        """
        Get per-benchmark scores for a specific round.

        Args:
            round_num: Round number to get scores for

        Returns:
            Dict mapping benchmark_name -> {provider_name: score}
        """
        result = {}
        for bm_name, history in self.benchmark_score_history.items():
            for r, scores in history:
                if r == round_num:
                    result[bm_name] = scores
                    break
        return result

    def evaluate_single(
        self,
        provider_name: str,
        true_capability: float,
        evaluation_engineering: float,
        round_num: int,
    ) -> float:
        """
        Evaluate a single provider with explicit ground truth.

        This is the preferred method for the new visibility architecture
        where ground truth is managed externally.

        Args:
            provider_name: Name of the provider
            true_capability: The provider's true capability (from simulation's ground truth)
            evaluation_engineering: How much the provider invested in benchmark optimization
            round_num: Current simulation round

        Returns:
            The benchmark score
        """
        return self.evaluate(true_capability, evaluation_engineering)

    def publish_scores(self, scores: dict) -> dict:
        """
        Publish scores (in current implementation, just returns scores).

        In a more complex simulation, this could involve:
        - Delayed publication
        - Partial information release
        - Leaderboard formatting

        Args:
            scores: Dict of {provider_name: score}

        Returns:
            Published scores (currently just the input)
        """
        return scores

    def get_leaderboard(self, scores: dict) -> list:
        """
        Return providers ranked by score.

        Args:
            scores: Dict of {provider_name: score}

        Returns:
            List of (provider_name, score) tuples, sorted descending by score
        """
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)

    def add_regulation(self, regulation: Regulation):
        """
        Add a regulation from a policymaker.

        Args:
            regulation: The regulation to add
        """
        self.active_regulations.append(regulation)

        # Apply regulation effects
        if regulation.regulation_type == "mandate_benchmark":
            # Could change benchmark parameters
            if "validity" in regulation.details:
                self.benchmark.validity = regulation.details["validity"]
            if "exploitability" in regulation.details:
                self.benchmark.exploitability = regulation.details["exploitability"]

        elif regulation.regulation_type == "set_threshold":
            # Store threshold for use in evaluation
            pass  # Future implementation

        elif regulation.regulation_type == "require_disclosure":
            # Could affect what information is published
            pass  # Future implementation

    def remove_regulation(self, regulation_name: str):
        """Remove a regulation by name."""
        self.active_regulations = [
            r for r in self.active_regulations if r.name != regulation_name
        ]

    def get_active_regulations(self) -> list[Regulation]:
        """Get list of active regulations."""
        return [r for r in self.active_regulations if r.active]

    def update_benchmark(self, aggregate_eval_engineering: float = 0.0):
        """
        Update benchmark properties based on gaming pressure.

        Gaming pressure (aggregate evaluation engineering investment) accelerates
        validity decay and exploitability growth, creating the core Goodhart's Law
        feedback loop: gaming degrades the benchmark, which incentivizes more gaming.

        Args:
            aggregate_eval_engineering: Average eval_engineering investment across providers
        """
        gaming_pressure = max(0.1, aggregate_eval_engineering)
        for bm in self.benchmarks:
            if bm.validity_decay_rate > 0:
                validity_decay = bm.validity_decay_rate * gaming_pressure
                bm.validity = max(0.2, bm.validity * (1 - validity_decay))

            if bm.exploitability_growth_rate > 0:
                exploitability_growth = bm.exploitability_growth_rate * gaming_pressure
                bm.exploitability = min(0.95, bm.exploitability * (1 + exploitability_growth))

        # Keep primary benchmark reference in sync
        self.benchmark = self.benchmarks[0]

    def consider_new_benchmark(self, round_num: int) -> Optional[Benchmark]:
        """
        Consider introducing a new benchmark based on ecosystem conditions.

        Triggers:
        - Any existing benchmark validity drops below 0.4 (degraded signal)
        - Periodic introduction every `cooldown` rounds

        Constraints:
        - 7-round cooldown between introductions
        - Maximum of max_benchmarks total benchmarks

        Returns:
            New Benchmark if introduced, None otherwise
        """
        # Check constraints
        if len(self.benchmarks) >= self.max_benchmarks:
            return None
        if round_num - self.last_introduction_round < self.benchmark_introduction_cooldown:
            return None

        # Check trigger conditions
        trigger = None

        # Trigger 1: Validity degradation
        for bm in self.benchmarks:
            if bm.validity < 0.4:
                trigger = f"validity_decay:{bm.name}={bm.validity:.2f}"
                break

        # Trigger 2: Periodic introduction (every cooldown rounds)
        if trigger is None and round_num > 0 and round_num % self.benchmark_introduction_cooldown == 0:
            trigger = f"periodic_introduction:round_{round_num}"

        if trigger is None:
            return None

        # Create new benchmark with fresh properties
        new_name = f"benchmark_r{round_num}"
        new_bm = Benchmark(
            name=new_name,
            validity=0.85,
            exploitability=0.15,
            noise_level=0.08,
            validity_decay_rate=self.benchmarks[0].validity_decay_rate,
            exploitability_growth_rate=self.benchmarks[0].exploitability_growth_rate,
        )

        # Weight = average of existing benchmark weights
        avg_weight = sum(self.benchmark_weights.values()) / len(self.benchmark_weights)
        self.benchmarks.append(new_bm)
        self.benchmark_weights[new_name] = avg_weight
        self.benchmark_score_history[new_name] = []
        self._best_published_scores[new_name] = {}

        # Record introduction
        self.last_introduction_round = round_num
        self.introduction_history.append({
            "round": round_num,
            "benchmark_name": new_name,
            "trigger": trigger,
        })

        return new_bm

    def compute_validity_correlation(self) -> Optional[float]:
        """
        Compute correlation between scores and true capabilities across history.

        This measures how well the benchmark is actually capturing true capability
        (i.e., is it still valid or has gaming corrupted it?).

        Returns:
            Pearson correlation coefficient, or None if insufficient data
        """
        if len(self.score_history) < 2:
            return None

        all_scores = []
        all_capabilities = []

        for (_, scores), (_, caps) in zip(self.score_history, self.capability_history):
            for name in scores:
                all_scores.append(scores[name])
                all_capabilities.append(caps[name])

        if len(all_scores) < 2:
            return None

        # Compute Pearson correlation
        scores_arr = np.array(all_scores)
        caps_arr = np.array(all_capabilities)

        correlation = np.corrcoef(scores_arr, caps_arr)[0, 1]
        return correlation

    def get_statistics(self) -> dict:
        """
        Get summary statistics about evaluation history.

        Returns:
            Dict with various statistics
        """
        stats = {
            "total_rounds": len(self.score_history),
            "num_benchmarks": len(self.benchmarks),
            "active_regulations": len(self.get_active_regulations()),
        }

        # Per-benchmark stats
        stats["benchmarks"] = {}
        for bm in self.benchmarks:
            stats["benchmarks"][bm.name] = {
                "validity": bm.validity,
                "exploitability": bm.exploitability,
                "noise": bm.noise_level,
                "weight": self.benchmark_weights.get(bm.name, 1.0),
            }

        # Primary benchmark for backwards compatibility
        stats["benchmark_validity"] = self.benchmark.validity
        stats["benchmark_exploitability"] = self.benchmark.exploitability
        stats["benchmark_noise"] = self.benchmark.noise_level

        # Compute validity correlation if possible
        correlation = self.compute_validity_correlation()
        if correlation is not None:
            stats["empirical_validity_correlation"] = correlation

        # Recent scores
        if self.score_history:
            recent_round, recent_scores = self.score_history[-1]
            stats["latest_round"] = recent_round
            stats["latest_scores"] = recent_scores

        return stats

    def get_benchmark_summary(self) -> str:
        """Get a summary of all benchmarks."""
        lines = [f"Evaluator with {len(self.benchmarks)} benchmark(s):"]
        for bm in self.benchmarks:
            weight = self.benchmark_weights.get(bm.name, 1.0)
            lines.append(f"  - {bm.name}: validity={bm.validity:.2f}, "
                        f"exploitability={bm.exploitability:.2f}, "
                        f"noise={bm.noise_level:.2f}, weight={weight:.1f}")
        return "\n".join(lines)

    def save(self, filepath: str):
        """Save evaluator state to JSON file."""
        data = {
            # Multi-benchmark data
            "benchmarks": [
                {
                    "name": bm.name,
                    "validity": bm.validity,
                    "exploitability": bm.exploitability,
                    "noise_level": bm.noise_level,
                    "validity_decay_rate": bm.validity_decay_rate,
                    "exploitability_growth_rate": bm.exploitability_growth_rate,
                    "weight": self.benchmark_weights.get(bm.name, 1.0),
                }
                for bm in self.benchmarks
            ],
            # Legacy single benchmark field for backwards compatibility
            "benchmark": {
                "name": self.benchmark.name,
                "validity": self.benchmark.validity,
                "exploitability": self.benchmark.exploitability,
                "noise_level": self.benchmark.noise_level,
                "validity_decay_rate": self.benchmark.validity_decay_rate,
                "exploitability_growth_rate": self.benchmark.exploitability_growth_rate,
            },
            "score_history": self.score_history,
            "benchmark_score_history": self.benchmark_score_history,
            "capability_history": self.capability_history,
            "current_round": self.current_round,
            "benchmark_introduction_cooldown": self.benchmark_introduction_cooldown,
            "last_introduction_round": self.last_introduction_round,
            "max_benchmarks": self.max_benchmarks,
            "introduction_history": self.introduction_history,
            "_best_published_scores": self._best_published_scores,
            "regulations": [
                {
                    "name": r.name,
                    "regulation_type": r.regulation_type,
                    "details": r.details,
                    "issued_round": r.issued_round,
                    "active": r.active,
                }
                for r in self.active_regulations
            ],
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls, filepath: str, seed: Optional[int] = None) -> "Evaluator":
        """Load evaluator state from JSON file."""
        with open(filepath, "r") as f:
            data = json.load(f)

        # Check for multi-benchmark data
        if "benchmarks" in data and len(data["benchmarks"]) > 0:
            benchmarks = data["benchmarks"]
            evaluator = cls(
                benchmarks=benchmarks,
                seed=seed,
            )
        else:
            # Legacy single benchmark format
            evaluator = cls(
                benchmark_name=data["benchmark"]["name"],
                validity=data["benchmark"]["validity"],
                exploitability=data["benchmark"]["exploitability"],
                noise_level=data["benchmark"]["noise_level"],
                seed=seed,
            )
            evaluator.benchmark.validity_decay_rate = data["benchmark"].get("validity_decay_rate", 0.0)
            evaluator.benchmark.exploitability_growth_rate = data["benchmark"].get("exploitability_growth_rate", 0.0)

        evaluator.score_history = data["score_history"]
        evaluator.capability_history = data["capability_history"]
        evaluator.current_round = data["current_round"]

        # Load benchmark score history if present
        if "benchmark_score_history" in data:
            evaluator.benchmark_score_history = data["benchmark_score_history"]

        # Load benchmark introduction state if present
        evaluator.benchmark_introduction_cooldown = data.get("benchmark_introduction_cooldown", 8)
        evaluator.last_introduction_round = data.get("last_introduction_round", 0)
        evaluator.max_benchmarks = data.get("max_benchmarks", 6)
        evaluator.introduction_history = data.get("introduction_history", [])

        # Load best published scores for monotonicity enforcement
        if "_best_published_scores" in data:
            evaluator._best_published_scores = data["_best_published_scores"]
        else:
            evaluator._best_published_scores = {bm.name: {} for bm in evaluator.benchmarks}

        # Load regulations if present
        if "regulations" in data:
            evaluator.active_regulations = [
                Regulation(**r) for r in data["regulations"]
            ]

        return evaluator

    def __repr__(self):
        return (
            f"Evaluator(benchmark='{self.benchmark.name}', "
            f"validity={self.benchmark.validity:.2f}, "
            f"exploitability={self.benchmark.exploitability:.2f})"
        )
