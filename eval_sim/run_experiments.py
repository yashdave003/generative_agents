"""
Run experiments with different actor configurations.

Experiment 1: 3 actors - Provider, Evaluator, Policymaker (no consumers)
Experiment 2: 4 actors - Provider, Evaluator, Consumer, Policymaker (all)
"""
import os
import sys

# Add eval_sim to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simulation import (
    EvalEcosystemSimulation,
    SimulationConfig,
    get_default_provider_configs,
)
from experiment_logger import ExperimentLogger, generate_summary
from game_log import generate_game_log_from_history


def run_experiment_with_config(
    name: str,
    description: str,
    tags: list,
    config: SimulationConfig,
    experiments_dir: str = "./experiments",
):
    """Run a single experiment with given configuration."""
    provider_configs = get_default_provider_configs()

    # Create experiment logger
    logger = ExperimentLogger(experiments_dir)
    exp_id = logger.create_experiment(
        name=name,
        description=description,
        tags=tags,
        seed=config.seed,
        llm_mode=config.llm_mode,
    )

    # Log config
    full_config = config.to_dict()
    full_config["provider_configs"] = provider_configs
    logger.log_config(full_config)

    # Run simulation
    sim = EvalEcosystemSimulation(config)
    sim.setup(provider_configs)
    sim.run()

    # Log results
    logger.log_history(sim.history)
    logger.log_summary(generate_summary(
        sim.history,
        sim.evaluator,
        sim.providers,
        consumers=sim.consumers if config.enable_consumers else None,
        policymakers=sim.policymakers if config.enable_policymakers else None,
    ))
    logger.log_providers(sim.providers)

    # Log ground truth
    logger.log_ground_truth(sim.ground_truth)

    # Log consumers if enabled
    if config.enable_consumers and sim.consumers:
        logger.log_consumers(sim.consumers)

    # Log policymakers if enabled
    if config.enable_policymakers and sim.policymakers:
        logger.log_policymakers(sim.policymakers)

    # Generate and save game log
    game_log_content = generate_game_log_from_history(
        history=sim.history,
        providers=sim.providers,
        experiment_name=name,
        experiment_id=exp_id,
        llm_mode=config.llm_mode,
        benchmark_params={
            "validity": config.benchmark_validity,
            "exploitability": config.benchmark_exploitability,
            "noise": config.benchmark_noise,
        },
        consumers=sim.consumers if config.enable_consumers else None,
        policymakers=sim.policymakers if config.enable_policymakers else None,
    )
    game_log_path = logger.save_game_log(game_log_content)
    print(f"Game log saved to: {game_log_path}")

    # Create plots
    try:
        import matplotlib
        matplotlib.use('Agg')
        from plotting import (
            plot_simulation_results,
            plot_strategy_evolution,
            plot_belief_accuracy,
            plot_validity_over_time,
            plot_consumer_satisfaction,
            plot_policymaker_interventions,
            plot_ecosystem_dashboard,
        )

        # Standard plots
        fig = plot_simulation_results(sim.history, show=False)
        if fig:
            logger.save_plot(fig, "simulation_overview.png")

        fig = plot_strategy_evolution(sim.history, show=False)
        if fig:
            logger.save_plot(fig, "strategy_evolution.png")

        fig = plot_belief_accuracy(sim.history, show=False)
        if fig:
            logger.save_plot(fig, "belief_accuracy.png")

        if len(sim.history) >= 5:
            fig = plot_validity_over_time(sim.history, show=False)
            if fig:
                logger.save_plot(fig, "validity_over_time.png")

        # Consumer plots
        if config.enable_consumers:
            fig = plot_consumer_satisfaction(sim.history, show=False)
            if fig:
                logger.save_plot(fig, "consumer_satisfaction.png")

        # Policymaker plots
        if config.enable_policymakers:
            fig = plot_policymaker_interventions(sim.history, show=False)
            if fig:
                logger.save_plot(fig, "policymaker_interventions.png")

        # Full ecosystem dashboard
        if config.enable_consumers or config.enable_policymakers:
            fig = plot_ecosystem_dashboard(sim.history, show=False)
            if fig:
                logger.save_plot(fig, "ecosystem_dashboard.png")

        print(f"Plots saved to: {logger.get_experiment_dir()}/plots/")

    except ImportError as e:
        print(f"Could not create plots: {e}")
    except Exception as e:
        print(f"Error creating plots: {e}")

    # Finalize
    logger.finalize()

    return exp_id, sim, logger


def main():
    """Run both experiments."""
    experiments_dir = os.path.join(os.path.dirname(__file__), "experiments")
    os.makedirs(experiments_dir, exist_ok=True)

    print("=" * 60)
    print("EXPERIMENT 1: 3 Actors (Provider, Evaluator, Policymaker)")
    print("=" * 60)
    print()

    config_3_actors = SimulationConfig(
        n_rounds=50,
        seed=42,
        benchmark_validity=0.7,
        benchmark_exploitability=0.5,
        benchmark_noise=0.1,
        enable_consumers=False,
        enable_policymakers=True,
        n_policymakers=1,
        verbose=True,
    )

    exp_id_1, sim_1, logger_1 = run_experiment_with_config(
        name="3_actors_no_consumer",
        description="Simulation with Provider, Evaluator, and Policymaker. No consumers.",
        tags=["3-actor", "policymaker", "no-consumer"],
        config=config_3_actors,
        experiments_dir=experiments_dir,
    )

    print()
    print("=" * 60)
    print("EXPERIMENT 2: 4 Actors (Provider, Evaluator, Consumer, Policymaker)")
    print("=" * 60)
    print()

    config_4_actors = SimulationConfig(
        n_rounds=50,
        seed=42,
        benchmark_validity=0.7,
        benchmark_exploitability=0.5,
        benchmark_noise=0.1,
        enable_consumers=True,
        enable_policymakers=True,
        n_consumers=10,
        n_policymakers=1,
        verbose=True,
    )

    exp_id_2, sim_2, logger_2 = run_experiment_with_config(
        name="4_actors_full_ecosystem",
        description="Full simulation with Provider, Evaluator, Consumer, and Policymaker.",
        tags=["4-actor", "full-ecosystem", "consumer", "policymaker"],
        config=config_4_actors,
        experiments_dir=experiments_dir,
    )

    # Print summary of heuristic experiments
    print()
    print("=" * 60)
    print("HEURISTIC EXPERIMENTS COMPLETE")
    print("=" * 60)
    print(f"Experiment 1: {exp_id_1}")
    print(f"  Location: {logger_1.get_experiment_dir()}")
    print(f"Experiment 2: {exp_id_2}")
    print(f"  Location: {logger_2.get_experiment_dir()}")
    print()

    # Print experiment index
    logger_1.print_summary()


def run_llm_experiments():
    """Run experiments with LLM mode enabled."""
    experiments_dir = os.path.join(os.path.dirname(__file__), "experiments")
    os.makedirs(experiments_dir, exist_ok=True)

    print()
    print("=" * 60)
    print("LLM MODE EXPERIMENTS")
    print("=" * 60)
    print()
    print("NOTE: LLM mode requires either:")
    print("  - OpenAI API key: export OPENAI_API_KEY=sk-...")
    print("  - Ollama running locally: export LLM_PROVIDER=ollama")
    print()

    # Experiment 3: 3 Actors with LLM
    print("=" * 60)
    print("EXPERIMENT 3: 3 Actors with LLM (Provider, Evaluator, Policymaker)")
    print("=" * 60)
    print()

    config_3_actors_llm = SimulationConfig(
        n_rounds=20,  # Fewer rounds (LLM is slower)
        seed=42,
        benchmark_validity=0.7,
        benchmark_exploitability=0.5,
        benchmark_noise=0.1,
        llm_mode=True,
        enable_consumers=False,
        enable_policymakers=True,
        n_policymakers=1,
        verbose=True,
    )

    exp_id_3, sim_3, logger_3 = run_experiment_with_config(
        name="3_actors_llm_mode",
        description="LLM-assisted simulation with Provider, Evaluator, and Policymaker. No consumers.",
        tags=["3-actor", "policymaker", "no-consumer", "llm"],
        config=config_3_actors_llm,
        experiments_dir=experiments_dir,
    )

    # Experiment 4: 4 Actors with LLM
    print()
    print("=" * 60)
    print("EXPERIMENT 4: 4 Actors with LLM (Full Ecosystem)")
    print("=" * 60)
    print()

    config_4_actors_llm = SimulationConfig(
        n_rounds=20,  # Fewer rounds (LLM is slower)
        seed=42,
        benchmark_validity=0.7,
        benchmark_exploitability=0.5,
        benchmark_noise=0.1,
        llm_mode=True,
        enable_consumers=True,
        enable_policymakers=True,
        n_consumers=10,
        n_policymakers=1,
        verbose=True,
    )

    exp_id_4, sim_4, logger_4 = run_experiment_with_config(
        name="4_actors_llm_mode",
        description="LLM-assisted full simulation with Provider, Evaluator, Consumer, and Policymaker.",
        tags=["4-actor", "full-ecosystem", "consumer", "policymaker", "llm"],
        config=config_4_actors_llm,
        experiments_dir=experiments_dir,
    )

    # Print summary
    print()
    print("=" * 60)
    print("LLM EXPERIMENTS COMPLETE")
    print("=" * 60)
    print(f"Experiment 3: {exp_id_3}")
    print(f"  Location: {logger_3.get_experiment_dir()}")
    print(f"Experiment 4: {exp_id_4}")
    print(f"  Location: {logger_4.get_experiment_dir()}")
    print()

    # Print experiment index
    logger_3.print_summary()

    return exp_id_3, exp_id_4


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run evaluation ecosystem experiments")
    parser.add_argument(
        "--llm",
        action="store_true",
        help="Run LLM mode experiments (requires API key or Ollama)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all experiments (heuristic and LLM)",
    )
    args = parser.parse_args()

    if args.all:
        main()
        run_llm_experiments()
    elif args.llm:
        run_llm_experiments()
    else:
        main()
