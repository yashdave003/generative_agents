"""Quick script to run LLM experiments with trace visibility and experiment logging.

Features:
- Real-time progress output (round timing, ETA)
- Automatic experiment logging to experiments/ directory
- LLM reasoning trace capture and export
- Configurable provider/benchmark/funder counts
"""
import os
import sys
import json
import time
from datetime import datetime

# Add eval_sim to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load .env file
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()
    print(f"Loaded environment from {env_path}")

from simulation import (
    EvalEcosystemSimulation, SimulationConfig,
    get_default_provider_configs, get_two_provider_configs,
)


def _format_duration(seconds: float) -> str:
    """Format seconds into human-readable duration."""
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        m, s = divmod(seconds, 60)
        return f"{int(m)}m {int(s)}s"
    else:
        h, remainder = divmod(seconds, 3600)
        m, s = divmod(remainder, 60)
        return f"{int(h)}h {int(m)}m {int(s)}s"


def run_quick_test(
    n_rounds: int = 5,
    provider: str = "openai",
    verbose_llm: bool = False,
    enable_ecosystem: bool = False,
    save_traces: str = None,
    log_experiment: bool = True,
    experiment_name: str = None,
    n_providers: int = 3,
    n_benchmarks: int = 1,
    enable_funders: bool = False,
):
    """Run a quick LLM test with optional trace logging and experiment logging.

    Args:
        n_rounds: Number of rounds to run
        provider: LLM provider (openai, anthropic, ollama, gemini)
        verbose_llm: If True, print raw LLM prompts and responses
        enable_ecosystem: If True, enable consumers and policymakers
        save_traces: If set, save full LLM reasoning traces to this file path
        log_experiment: If True, log to experiments/ directory
        experiment_name: Custom experiment name (auto-generated if None)
        n_providers: Number of providers (2 or 3)
        n_benchmarks: Number of benchmarks (1 or 2)
        enable_funders: If True, enable funder actors
    """
    os.environ["LLM_PROVIDER"] = provider

    # Build configuration description
    parts = []
    parts.append(f"{n_providers} providers")
    parts.append(f"{n_benchmarks} benchmark{'s' if n_benchmarks > 1 else ''}")
    parts.append(f"{n_rounds} rounds")
    if enable_ecosystem:
        parts.append("6 consumers")
        parts.append("1 policymaker")
    if enable_funders:
        parts.append("1 funder")
    if verbose_llm:
        parts.append("verbose traces ON")

    print()
    print("=" * 60)
    print(f"LLM EXPERIMENT ({provider.upper()})")
    print(", ".join(parts))
    print("=" * 60)
    print()

    # Provider configs
    if n_providers == 2:
        provider_configs = get_two_provider_configs()
    else:
        provider_configs = get_default_provider_configs()

    if verbose_llm:
        for pc in provider_configs:
            pc["verbose_llm"] = True

    # Benchmark configs
    benchmarks = None
    if n_benchmarks >= 2:
        benchmarks = [
            {
                "name": "capability_bench",
                "validity": 0.8,
                "exploitability": 0.3,
                "noise_level": 0.1,
                "weight": 0.6,
            },
            {
                "name": "safety_bench",
                "validity": 0.6,
                "exploitability": 0.5,
                "noise_level": 0.1,
                "weight": 0.4,
            },
        ]

    # Funder configs
    funder_configs = None
    if enable_funders:
        from actors.funder import get_default_funder_configs
        funder_configs = get_default_funder_configs()

    config = SimulationConfig(
        n_rounds=n_rounds,
        seed=42,
        benchmark_validity=0.7,
        benchmark_exploitability=0.5,
        benchmark_noise=0.1,
        benchmarks=benchmarks,
        llm_mode=True,
        enable_consumers=enable_ecosystem,
        enable_policymakers=enable_ecosystem,
        enable_funders=enable_funders,
        n_consumers=6 if enable_ecosystem else 0,
        n_policymakers=1 if enable_ecosystem else 0,
        n_funders=len(funder_configs) if funder_configs else 0,
        verbose=True,
    )

    # --- Experiment logging setup ---
    logger = None
    exp_id = None
    if log_experiment:
        from experiment_logger import ExperimentLogger
        experiments_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "experiments")
        logger = ExperimentLogger(experiments_dir)

        if experiment_name is None:
            experiment_name = f"{n_providers}p_{n_benchmarks}b_{n_rounds}r_{provider}"
            if enable_ecosystem:
                experiment_name += "_ecosystem"
            if enable_funders:
                experiment_name += "_funders"

        tags = ["llm", provider, f"{n_providers}-provider"]
        if enable_ecosystem:
            tags.append("ecosystem")
        if enable_funders:
            tags.append("funders")

        exp_id = logger.create_experiment(
            name=experiment_name,
            description=(
                f"LLM-driven simulation: {n_providers} providers, {n_benchmarks} benchmarks, "
                f"{n_rounds} rounds using {provider}. "
                f"{'With consumers + policymaker. ' if enable_ecosystem else ''}"
                f"{'With funders. ' if enable_funders else ''}"
            ),
            tags=tags,
            seed=config.seed,
            llm_mode=True,
        )

        full_config = config.to_dict()
        full_config["provider_configs"] = provider_configs
        if funder_configs:
            full_config["funder_configs"] = funder_configs
        logger.log_config(full_config)

        print(f"Experiment: {exp_id}")
        print(f"Logging to: {logger.get_experiment_dir()}")
        print()

    # --- Run simulation with progress tracking ---
    sim = EvalEcosystemSimulation(config)
    sim.setup(
        provider_configs=provider_configs,
        funder_configs=funder_configs,
    )

    print(f"=== Running {n_rounds} rounds ===\n")

    start = time.time()
    round_times = []

    for i in range(n_rounds):
        round_start = time.time()

        # Progress header
        elapsed = round_start - start
        if round_times:
            avg_round_time = sum(round_times) / len(round_times)
            remaining_rounds = n_rounds - i
            eta = avg_round_time * remaining_rounds
            print(f"[Round {i}/{n_rounds}] "
                  f"Elapsed: {_format_duration(elapsed)} | "
                  f"ETA: {_format_duration(eta)} | "
                  f"Avg/round: {_format_duration(avg_round_time)}")
        elif i == 0:
            print(f"[Round {i}/{n_rounds}] Starting...")

        # Run the round (verbose output comes from sim._print_round_summary)
        round_data = sim.run_round()
        if logger:
            logger.log_round(round_data)

        round_elapsed = time.time() - round_start
        round_times.append(round_elapsed)

    # Final summary
    sim._print_final_summary()

    total_elapsed = time.time() - start
    print()
    print("=" * 60)
    print(f"COMPLETE ({_format_duration(total_elapsed)})")
    if round_times:
        print(f"  Avg round time: {_format_duration(sum(round_times) / len(round_times))}")
        print(f"  Fastest round: {_format_duration(min(round_times))}")
        print(f"  Slowest round: {_format_duration(max(round_times))}")
    print("=" * 60)

    # --- Save traces ---
    if save_traces:
        traces = _collect_all_traces(sim)
        with open(save_traces, "w") as f:
            json.dump(traces, f, indent=2)
        print(f"Traces saved to: {save_traces}")

    # --- Log experiment results ---
    if logger:
        from experiment_logger import generate_summary
        from game_log import generate_game_log_from_history

        # History and summary
        logger.log_history(sim.history)
        logger.log_summary(generate_summary(
            sim.history,
            sim.evaluator,
            sim.providers,
            consumers=sim.consumer_market if config.enable_consumers else None,
            policymakers=sim.policymakers if config.enable_policymakers else None,
            funders=sim.funders if config.enable_funders else None,
        ))

        # Actor states
        logger.log_providers(sim.providers)
        logger.log_ground_truth(sim.ground_truth)

        if config.enable_consumers and sim.consumer_market:
            logger.log_consumers(sim.consumer_market)
        if config.enable_policymakers and sim.policymakers:
            logger.log_policymakers(sim.policymakers)
        if config.enable_funders and sim.funders:
            logger.log_funders(sim.funders)

        # Game log
        benchmark_params = {
            "validity": config.benchmark_validity,
            "exploitability": config.benchmark_exploitability,
            "noise": config.benchmark_noise,
        }
        game_log_content = generate_game_log_from_history(
            history=sim.history,
            providers=sim.providers,
            experiment_name=experiment_name,
            experiment_id=exp_id,
            llm_mode=True,
            benchmark_params=benchmark_params,
            benchmarks=benchmarks,
            policymakers=sim.policymakers if config.enable_policymakers else None,
        )
        logger.save_game_log(game_log_content)

        # Plots
        try:
            import matplotlib
            matplotlib.use('Agg')
            from plotting import create_all_dashboards

            plot_metadata = {
                "n_rounds": config.n_rounds,
                "llm_mode": config.llm_mode,
                "n_consumers": len(sim.consumer_market.segments) if config.enable_consumers and sim.consumer_market else 0,
                "n_policymakers": config.n_policymakers if config.enable_policymakers else 0,
                "n_funders": config.n_funders if config.enable_funders else 0,
            }
            plots_dir = os.path.join(logger.get_experiment_dir(), "plots")
            create_all_dashboards(sim.history, plots_dir, show=False, metadata=plot_metadata)
        except Exception as e:
            print(f"Could not create plots: {e}")

        # Add timing note
        logger.add_note(f"Total runtime: {_format_duration(total_elapsed)}")
        if round_times:
            logger.add_note(f"Avg round time: {_format_duration(sum(round_times) / len(round_times))}")

        logger.finalize()
        print(f"\nExperiment saved: {logger.get_experiment_dir()}")

    return sim


def _collect_all_traces(sim) -> dict:
    """Collect all LLM reasoning traces from the simulation."""
    traces = {
        "rounds": [],
        "provider_insights": {},
    }

    # Per-round traces from history
    for rd in sim.history:
        round_traces = {
            "round": rd["round"],
            "leaderboard": sorted(rd["scores"].items(), key=lambda x: x[1], reverse=True),
        }
        if "actor_traces" in rd:
            round_traces["reasoning"] = rd["actor_traces"]
        traces["rounds"].append(round_traces)

    # Per-provider full memory (includes all planning + reflection reasoning)
    for provider in sim.providers:
        insights = []
        for entry in provider.memory:
            if entry.get("type") in ("planning", "reflection") and entry.get("reasoning"):
                insights.append({
                    "round": entry.get("round"),
                    "type": entry["type"],
                    "reasoning": entry["reasoning"],
                    "portfolio": entry.get("portfolio"),
                })
        traces["provider_insights"][provider.name] = insights

    return traces


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Run LLM experiments with logging and progress tracking",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick 3-round test with Ollama
  python run_llm_now.py -r 3 -p ollama

  # Full ecosystem with funders, logged
  python run_llm_now.py -r 5 -p openai -e --funders

  # 2 providers, 2 benchmarks, no logging
  python run_llm_now.py -r 3 --providers 2 --benchmarks 2 --no-log

  # Verbose traces + save to file
  python run_llm_now.py -r 3 -p ollama -v -s traces.json
        """,
    )
    parser.add_argument("--rounds", "-r", type=int, default=5, help="Number of rounds")
    parser.add_argument("--provider", "-p", default="openai",
                        choices=["openai", "anthropic", "ollama", "gemini"])
    parser.add_argument("--providers", type=int, default=3, choices=[2, 3],
                        help="Number of model providers (2 or 3)")
    parser.add_argument("--benchmarks", type=int, default=1, choices=[1, 2],
                        help="Number of benchmarks (1 or 2)")
    parser.add_argument("--verbose-llm", "-v", action="store_true",
                        help="Print raw LLM prompts and responses")
    parser.add_argument("--ecosystem", "-e", action="store_true",
                        help="Enable consumers and policymakers")
    parser.add_argument("--funders", action="store_true",
                        help="Enable funder actors")
    parser.add_argument("--save-traces", "-s", type=str, default=None,
                        help="Save LLM reasoning traces to JSON file")
    parser.add_argument("--no-log", action="store_true",
                        help="Disable experiment logging to experiments/")
    parser.add_argument("--name", type=str, default=None,
                        help="Custom experiment name")
    args = parser.parse_args()

    run_quick_test(
        n_rounds=args.rounds,
        provider=args.provider,
        verbose_llm=args.verbose_llm,
        enable_ecosystem=args.ecosystem,
        save_traces=args.save_traces,
        log_experiment=not args.no_log,
        experiment_name=args.name,
        n_providers=args.providers,
        n_benchmarks=args.benchmarks,
        enable_funders=args.funders,
    )
