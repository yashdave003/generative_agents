"""Quick script to run LLM experiments."""
import os
import sys

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

from simulation import EvalEcosystemSimulation, SimulationConfig, get_default_provider_configs


def run_quick_test(n_rounds: int = 5, provider: str = "openai"):
    """Run a minimal LLM test with 2 actors, 1 benchmark."""
    os.environ["LLM_PROVIDER"] = provider

    print()
    print("=" * 60)
    print(f"QUICK LLM TEST ({provider.upper()})")
    print(f"2 actors, 1 benchmark, {n_rounds} rounds")
    print("=" * 60)
    print()

    config = SimulationConfig(
        n_rounds=n_rounds,
        seed=42,
        benchmark_validity=0.7,
        benchmark_exploitability=0.5,
        benchmark_noise=0.1,
        llm_mode=True,
        enable_consumers=False,
        enable_policymakers=False,
        verbose=True,
    )

    sim = EvalEcosystemSimulation(config)
    sim.setup(get_default_provider_configs())
    sim.run()

    print()
    print("=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

    return sim


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run quick LLM test")
    parser.add_argument("--rounds", "-r", type=int, default=5, help="Number of rounds")
    parser.add_argument("--provider", "-p", default="openai", choices=["openai", "ollama"])
    args = parser.parse_args()

    run_quick_test(n_rounds=args.rounds, provider=args.provider)
