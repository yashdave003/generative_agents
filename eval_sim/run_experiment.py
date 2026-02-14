"""
Experiment Configuration & Runner
==================================
Edit the config below, then run:  python run_experiment.py

For quick CLI-driven tests, use run_llm_now.py instead.
"""
import os
import sys
import time

# Prevent CPU thread oversubscription on shared clusters
n_threads_str = "4"
os.environ["OMP_NUM_THREADS"] = n_threads_str
os.environ["OPENBLAS_NUM_THREADS"] = n_threads_str
os.environ["MKL_NUM_THREADS"] = n_threads_str
os.environ["VECLIB_MAXIMUM_THREADS"] = n_threads_str
os.environ["NUMEXPR_NUM_THREADS"] = n_threads_str

# ============================================================
#  EXPERIMENT CONFIG -- edit everything here
# ============================================================

EXPERIMENT = {
    "name": "5p_2b_3funder_highcap",
    "description": (
        "Full ecosystem v6: 5 providers, 2 benchmarks (coding + reasoning), "
        "30 consumer segments (10 use-cases × 3 archetypes), 1 policymaker,"
        "3 funders (2 VC + 1 Gov) with high capital ($2B/$500M/$100M). "
        "NEW v6 features: funder diversification (observe other funders' allocations), "
        "per-benchmark score reporting (console output), optional benchmark sequence. "
        "Funder rework: 10% per-round deployment cap, 2-round cooldown, "
        "momentum-based scoring with diversification signal. "
        "LLM mode via Ollama."
    ),
    "tags": ["llm", "ollama", "5-provider", "2-benchmark", "12-segments",
             "3-funder", "high-capital", "funder-diversification", "per-benchmark-reporting",
             "full-ecosystem-v6"],
}

LLM = {
    "provider": "ollama",       # openai | anthropic | ollama | gemini
    "llm_mode": False,          # True = LLM planning, False = heuristic
}

SIMULATION = {
    "n_rounds": 30,
    "seed": 42,
    "verbose": True,
    "rnd_efficiency": 0.01,
    # S-curve
    "capability_ceiling": 1.0,
    "diminishing_returns_rate": 3.0,
    "breakthrough_probability": 0.02,
    "breakthrough_magnitude": 0.05,
    # Benchmark evolution
    "benchmark_validity_decay_rate": 0.005,
    "benchmark_exploitability_growth_rate": 0.008,
    # Benchmark introduction
    "benchmark_introduction_cooldown": 6,
    "max_benchmarks": 6,
    # Pre-defined benchmark sequence (meaningful names instead of auto-generated)
    "benchmark_sequence": [
        {"name": "logical_reasoning", "validity": 0.5, "exploitability": 0.15, "noise_level": 0.08, "weight": 1.0},
        {"name": "advanced_coding", "validity": 0.85, "exploitability": 0.15, "noise_level": 0.08, "weight": 1.0},
        {"name": "factual_recall", "validity": 0.4, "exploitability": 0.50, "noise_level": 0.09, "weight": 1.0},
        {"name": "science", "validity": 0.70, "exploitability": 0.25, "noise_level": 0.10, "weight": 1.0},
    ],
    # To disable sequence and use auto-generation, set to None:
    # "benchmark_sequence": None,
    # Media
    "enable_media": True,
    # Consumer market: 10 use-cases × 3 archetypes = 30 segments
    "use_case_profiles": ["software_dev", "content_writer", "legal", "healthcare", "finance",
                          "customer_service", "researcher", "creative", "marketing", "service_worker"],
}

# 2 benchmarks: coding (high validity, harder to game) and reasoning (more exploitable)
BENCHMARKS = [
    {"name": "coding_bench", "validity": 0.55, "exploitability": 0.35,
     "noise_level": 0.08, "weight": 0.5},
    {"name": "question_answering_bench", "validity": 0.7, "exploitability": 0.45,
     "noise_level": 0.1, "weight": 0.5},
]

# 5 providers: OpenAI, Anthropic, NovaMind, DeepMind, Meta_AI
PROVIDERS = "five"

CONSUMERS = {
    "enabled": True,
    # 4 use_case_profiles × 3 archetypes = 12 market segments
}

POLICYMAKERS = {
    "enabled": True,
    "n_policymakers": 1,
}

FUNDERS = {
    "enabled": True,
    "configs": [
        {
            "name": "TechVentures",
            "funder_type": "vc",
            "total_capital": 2_000_000_000.0,
            "risk_tolerance": 0.9,
            "mission_statement": "Early-stage AI startup bets with outsized upside potential",
            "max_round_deployment": 0.15,
            "funding_cooldown": 3,
        },
        {
            "name": "Horizon_Capital",
            "funder_type": "vc",
            "total_capital": 500_000_000.0,
            "risk_tolerance": 0.6,
            "mission_statement": "Maximize returns by backing AI market leaders",
            "max_round_deployment": 0.10,
            "funding_cooldown": 2,
        },
        {
            "name": "AISI_Fund",
            "funder_type": "gov",
            "total_capital": 100_000_000.0,
            "risk_tolerance": 0.3,
            "mission_statement": "Ensure safe and responsible AI development",
            "max_round_deployment": 0.10,
            "funding_cooldown": 4,
        },
    ],
}


# ============================================================
#  RUNNER -- no need to edit below this line
# ============================================================

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


def run():
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

    os.environ["LLM_PROVIDER"] = LLM["provider"]

    from simulation import (
        EvalEcosystemSimulation, SimulationConfig,
        get_default_provider_configs, get_two_provider_configs, get_five_provider_configs,
    )
    from experiment_logger import ExperimentLogger, generate_summary
    from game_log import generate_game_log_from_history

    # --- Resolve provider configs ---
    if isinstance(PROVIDERS, str):
        if PROVIDERS == "five":
            provider_configs = get_five_provider_configs()
        elif PROVIDERS == "two":
            provider_configs = get_two_provider_configs()
        else:
            provider_configs = get_default_provider_configs()
    else:
        provider_configs = PROVIDERS

    # --- Resolve funder configs ---
    funder_configs = FUNDERS.get("configs") if FUNDERS["enabled"] else None
    if FUNDERS["enabled"] and funder_configs is None:
        from actors.funder import get_multi_funder_configs
        funder_configs = get_multi_funder_configs()

    n_funders = len(funder_configs) if funder_configs else 0
    n_rounds = SIMULATION["n_rounds"]

    # --- Build SimulationConfig ---
    config = SimulationConfig(
        n_rounds=n_rounds,
        seed=SIMULATION.get("seed", 42),
        benchmark_validity=0.7,
        benchmark_exploitability=0.5,
        benchmark_noise=0.1,
        benchmarks=BENCHMARKS,
        rnd_efficiency=SIMULATION.get("rnd_efficiency", 0.01),
        capability_ceiling=SIMULATION.get("capability_ceiling", 1.0),
        diminishing_returns_rate=SIMULATION.get("diminishing_returns_rate", 3.0),
        breakthrough_probability=SIMULATION.get("breakthrough_probability", 0.02),
        breakthrough_magnitude=SIMULATION.get("breakthrough_magnitude", 0.05),
        benchmark_validity_decay_rate=SIMULATION.get("benchmark_validity_decay_rate", 0.005),
        benchmark_exploitability_growth_rate=SIMULATION.get("benchmark_exploitability_growth_rate", 0.008),
        benchmark_introduction_cooldown=SIMULATION.get("benchmark_introduction_cooldown", 6),
        max_benchmarks=SIMULATION.get("max_benchmarks", 6),
        benchmark_sequence=SIMULATION.get("benchmark_sequence"),
        llm_mode=LLM["llm_mode"],
        enable_consumers=CONSUMERS["enabled"],
        enable_policymakers=POLICYMAKERS["enabled"],
        enable_funders=FUNDERS["enabled"],
        enable_media=SIMULATION.get("enable_media", False),
        n_policymakers=POLICYMAKERS.get("n_policymakers", 1) if POLICYMAKERS["enabled"] else 0,
        n_funders=n_funders,
        use_case_profiles=SIMULATION.get("use_case_profiles"),
        verbose=SIMULATION.get("verbose", True),
    )

    # --- Print banner ---
    parts = [
        f"{len(provider_configs)} providers",
        f"{n_rounds} rounds",
        f"LLM={LLM['provider']}" if LLM["llm_mode"] else "heuristic",
    ]
    if CONSUMERS["enabled"]:
        n_use_cases = len(SIMULATION.get("use_case_profiles", [])) or 6
        parts.append(f"{n_use_cases * 3} consumer segments")
    if POLICYMAKERS["enabled"]:
        parts.append(f"{config.n_policymakers} policymaker(s)")
    if FUNDERS["enabled"]:
        parts.append(f"{n_funders} funder(s)")
    if SIMULATION.get("enable_media"):
        parts.append("media")

    print()
    print("=" * 70)
    print(f"EXPERIMENT: {EXPERIMENT['name']}")
    print(", ".join(parts))
    print("=" * 70)
    print()

    # --- Experiment logging setup ---
    experiments_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "experiments")
    # Use heuristic subdirectory for heuristic runs (separate numbering)
    use_heuristic_subdir = not config.llm_mode
    logger = ExperimentLogger(experiments_dir, use_heuristic_subdir=use_heuristic_subdir)
    exp_id = logger.create_experiment(
        name=EXPERIMENT["name"],
        description=EXPERIMENT.get("description", ""),
        tags=EXPERIMENT.get("tags", []),
        seed=config.seed,
        llm_mode=config.llm_mode,
    )

    full_config = config.to_dict()
    full_config["provider_configs"] = provider_configs
    if funder_configs:
        full_config["funder_configs"] = funder_configs
    logger.log_config(full_config)

    print(f"Experiment: {exp_id}")
    print(f"Logging to: {logger.get_experiment_dir()}")
    print()

    # --- Run simulation with per-round progress ---
    sim = EvalEcosystemSimulation(config)
    sim.setup(
        provider_configs=provider_configs,
        funder_configs=funder_configs,
    )

    print(f"=== Running {n_rounds} rounds ===\n")

    # Prepare plotting for incremental saves (LLM mode only)
    plot_metadata = {
        "n_rounds": config.n_rounds,
        "llm_mode": config.llm_mode,
        "n_consumers": 0,  # Will update after setup
        "n_policymakers": config.n_policymakers if config.enable_policymakers else 0,
        "n_funders": config.n_funders if config.enable_funders else 0,
    }
    if config.enable_consumers and sim.consumer_market:
        plot_metadata["n_consumers"] = len(sim.consumer_market.segments)

    plots_dir = os.path.join(logger.get_experiment_dir(), "plots")

    # Import matplotlib once
    matplotlib_available = False
    try:
        import matplotlib
        matplotlib.use('Agg')
        from plotting import create_all_dashboards
        matplotlib_available = True
    except Exception as e:
        print(f"Warning: Matplotlib not available, plots will be skipped: {e}")

    def save_plots_if_needed(round_num: int, force: bool = False):
        """Save plots every 10 rounds (in LLM mode) or when forced."""
        if not matplotlib_available:
            return
        # Only do incremental saves in LLM mode (heuristic is fast anyway)
        if not force and not config.llm_mode:
            return
        if not force and (round_num + 1) % 10 != 0:
            return
        try:
            create_all_dashboards(sim.history, plots_dir, show=False, metadata=plot_metadata)
            if not force:
                print(f"  → Plots saved (round {round_num})")
        except Exception as e:
            print(f"  → Could not save plots: {e}")

    start = time.time()
    round_times = []

    for i in range(n_rounds):
        round_start = time.time()

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

        round_data = sim.run_round()
        logger.log_round(round_data)

        round_elapsed = time.time() - round_start
        round_times.append(round_elapsed)

        # Save plots every 10 rounds (LLM mode only)
        save_plots_if_needed(i)

    sim._print_final_summary()

    total_elapsed = time.time() - start

    print()
    print("=" * 70)
    print(f"SIMULATION COMPLETE - Total time: {_format_duration(total_elapsed)}")
    if round_times:
        print(f"  Avg round: {_format_duration(sum(round_times) / len(round_times))}")
        print(f"  Fastest:   {_format_duration(min(round_times))}")
        print(f"  Slowest:   {_format_duration(max(round_times))}")
    print("=" * 70)

    # --- Log results ---
    logger.log_history(sim.history)
    logger.log_summary(generate_summary(
        sim.history,
        sim.evaluator,
        sim.providers,
        consumers=sim.consumer_market if config.enable_consumers else None,
        policymakers=sim.policymakers if config.enable_policymakers else None,
        funders=sim.funders if config.enable_funders else None,
    ))
    logger.log_providers(sim.providers)
    logger.log_ground_truth(sim.ground_truth)

    if config.enable_consumers and sim.consumer_market:
        logger.log_consumers(sim.consumer_market)
    if config.enable_policymakers and sim.policymakers:
        logger.log_policymakers(sim.policymakers)
    if config.enable_funders and sim.funders:
        logger.log_funders(sim.funders)

    # Game log
    game_log_content = generate_game_log_from_history(
        history=sim.history,
        providers=sim.providers,
        experiment_name=EXPERIMENT["name"],
        experiment_id=exp_id,
        llm_mode=config.llm_mode,
        benchmark_params={
            "validity": config.benchmark_validity,
            "exploitability": config.benchmark_exploitability,
            "noise": config.benchmark_noise,
        },
        benchmarks=BENCHMARKS,
        policymakers=sim.policymakers if config.enable_policymakers else None,
    )
    game_log_path = logger.save_game_log(game_log_content)
    print(f"Game log saved to: {game_log_path}")

    # Final plots (force save regardless of round number)
    save_plots_if_needed(n_rounds - 1, force=True)

    # Finalize
    logger.add_note(f"Total runtime: {_format_duration(total_elapsed)}")
    if round_times:
        logger.add_note(f"Avg round time: {_format_duration(sum(round_times) / len(round_times))}")
    logger.finalize()

    print(f"\nExperiment saved to: {logger.get_experiment_dir()}")

    return sim


if __name__ == "__main__":
    run()
