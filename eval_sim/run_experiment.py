"""
Experiment Configuration & Runner
==================================
Edit the config below, then run:  python run_experiment.py

For quick CLI-driven tests, use run_llm_now.py instead.
"""
import os
import sys
import time

# ============================================================
#  EXPERIMENT CONFIG -- edit everything here
# ============================================================

EXPERIMENT = {
    "name": "5p_2b_full_ecosystem_v4",
    "description": (
        "Full ecosystem v4: 5 providers, 2 benchmarks (coding + reasoning), "
        "12 consumer segments (4 use-cases × 3 archetypes), 1 policymaker, "
        "4 funders, expanded media actor (TechPress). "
        "New in v4: monotonic per-benchmark scores (providers don't disclose worse scores), "
        "periodic benchmark introduction every 7 rounds (replaces every-15-round trigger), "
        "expanded media reporting (funding headlines, per-benchmark leader changes, "
        "consumer market shifts, narrative framing of large score jumps, "
        "specific policymaker intervention headlines). "
        "LLM mode via Ollama."
    ),
    "tags": ["llm", "ollama", "5-provider", "2-benchmark", "12-segments",
             "4-funder", "media-expanded", "monotonic-scores",
             "periodic-benchmarks", "full-ecosystem-v4"],
}

LLM = {
    "provider": "ollama",       # openai | anthropic | ollama | gemini
    "llm_mode": True,           # True = LLM planning, False = heuristic
}

SIMULATION = {
    "n_rounds": 10,
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
    "benchmark_introduction_cooldown": 7,
    "max_benchmarks": 6,
    # Media
    "enable_media": True,
    # Consumer market: 4 use-cases × 3 archetypes = 12 segments
    "use_case_profiles": ["software_dev", "content_writer", "healthcare", "finance"],
}

# 2 benchmarks: coding (high validity, harder to game) and reasoning (more exploitable)
BENCHMARKS = [
    {"name": "coding_bench", "validity": 0.85, "exploitability": 0.25,
     "noise_level": 0.08, "weight": 0.5},
    {"name": "reasoning_bench", "validity": 0.7, "exploitability": 0.45,
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
            "total_capital": 10000000.0,
            "risk_tolerance": 0.7,
            "mission_statement": "Maximize returns by backing AI market leaders",
            "max_round_deployment": 0.10,
            "funding_cooldown": 2,
        },
        {
            "name": "Horizon_Capital",
            "funder_type": "vc",
            "total_capital": 5000000.0,
            "risk_tolerance": 0.85,
            "mission_statement": "Early-stage AI bets with outsized upside potential",
            "max_round_deployment": 0.10,
            "funding_cooldown": 2,
        },
        {
            "name": "AISI_Fund",
            "funder_type": "gov",
            "total_capital": 500000.0,
            "risk_tolerance": 0.3,
            "mission_statement": "Ensure safe and responsible AI development",
            "max_round_deployment": 0.10,
            "funding_cooldown": 2,
        },
        {
            "name": "OpenResearch",
            "funder_type": "foundation",
            "total_capital": 300000.0,
            "risk_tolerance": 0.5,
            "mission_statement": "Support authentic capability advancement for societal benefit",
            "max_round_deployment": 0.10,
            "funding_cooldown": 2,
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
    logger = ExperimentLogger(experiments_dir)
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

    # Finalize
    logger.add_note(f"Total runtime: {_format_duration(total_elapsed)}")
    if round_times:
        logger.add_note(f"Avg round time: {_format_duration(sum(round_times) / len(round_times))}")
    logger.finalize()

    print(f"\nExperiment saved to: {logger.get_experiment_dir()}")

    return sim


if __name__ == "__main__":
    run()
