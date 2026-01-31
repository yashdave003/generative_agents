"""
Plotting utilities for Evaluation Ecosystem Simulation

Visualizes simulation dynamics over time.
"""
import matplotlib.pyplot as plt
import numpy as np
from typing import Optional


def plot_simulation_results(
    history: list[dict],
    save_path: Optional[str] = None,
    show: bool = True,
):
    """
    Create a comprehensive plot of simulation results.

    Args:
        history: List of round data dicts from simulation
        save_path: If provided, save figure to this path
        show: Whether to display the plot
    """
    if not history:
        print("No history to plot")
        return

    # Extract data
    rounds = [h["round"] for h in history]
    providers = list(history[0]["scores"].keys())

    # Use a color scheme that works well
    colors = {providers[0]: "#E63946", providers[1]: "#457B9D"}  # Red, Blue

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Evaluation Ecosystem Simulation Results", fontsize=14, fontweight="bold")

    # --- Plot 1: Scores over time ---
    ax1 = axes[0, 0]
    for provider in providers:
        scores = [h["scores"][provider] for h in history]
        ax1.plot(rounds, scores, "o-", label=f"{provider}", color=colors[provider],
                 markersize=4, linewidth=1.5, alpha=0.8)
    ax1.set_xlabel("Round")
    ax1.set_ylabel("Benchmark Score")
    ax1.set_title("Benchmark Scores Over Time")
    ax1.legend(loc="best")
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1)

    # --- Plot 2: True Capability vs Believed Capability ---
    ax2 = axes[0, 1]
    for provider in providers:
        true_caps = [h["true_capabilities"][provider] for h in history]
        believed_caps = [h["believed_capabilities"][provider] for h in history]

        ax2.plot(rounds, true_caps, "-", label=f"{provider} (true)",
                 color=colors[provider], linewidth=2)
        ax2.plot(rounds, believed_caps, "--", label=f"{provider} (believed)",
                 color=colors[provider], linewidth=1.5, alpha=0.7)

    ax2.set_xlabel("Round")
    ax2.set_ylabel("Capability")
    ax2.set_title("True vs Believed Capability")
    ax2.legend(loc="best", fontsize=8)
    ax2.grid(True, alpha=0.3)

    # --- Plot 3: Strategy Allocation Over Time ---
    ax3 = axes[1, 0]
    bar_width = 0.35
    x = np.array(rounds)

    for i, provider in enumerate(providers):
        rnd_inv = [h["strategies"][provider]["rnd"] for h in history]
        gaming_inv = [h["strategies"][provider]["gaming"] for h in history]

        offset = (i - 0.5) * bar_width
        ax3.bar(x + offset, rnd_inv, bar_width * 0.9, label=f"{provider} R&D",
                color=colors[provider], alpha=0.7)
        ax3.bar(x + offset, gaming_inv, bar_width * 0.9, bottom=rnd_inv,
                label=f"{provider} Gaming", color=colors[provider], alpha=0.3,
                hatch="//")

    ax3.set_xlabel("Round")
    ax3.set_ylabel("Investment Allocation")
    ax3.set_title("Strategy Allocation (R&D vs Gaming)")
    ax3.legend(loc="upper right", fontsize=8)
    ax3.set_ylim(0, 1.1)
    ax3.axhline(y=0.5, color="gray", linestyle=":", alpha=0.5)
    ax3.grid(True, alpha=0.3, axis="y")

    # --- Plot 4: Score vs True Capability (Validity Check) ---
    ax4 = axes[1, 1]
    for provider in providers:
        scores = [h["scores"][provider] for h in history]
        true_caps = [h["true_capabilities"][provider] for h in history]

        ax4.scatter(true_caps, scores, label=provider, color=colors[provider],
                    alpha=0.6, s=50)

    # Add diagonal line (perfect validity)
    all_vals = []
    for provider in providers:
        all_vals.extend([h["scores"][provider] for h in history])
        all_vals.extend([h["true_capabilities"][provider] for h in history])
    min_val, max_val = min(all_vals), max(all_vals)
    ax4.plot([min_val, max_val], [min_val, max_val], "k--", alpha=0.3,
             label="Perfect validity")

    # Compute and show correlation
    all_scores = []
    all_caps = []
    for provider in providers:
        all_scores.extend([h["scores"][provider] for h in history])
        all_caps.extend([h["true_capabilities"][provider] for h in history])
    correlation = np.corrcoef(all_scores, all_caps)[0, 1]

    ax4.set_xlabel("True Capability")
    ax4.set_ylabel("Benchmark Score")
    ax4.set_title(f"Score vs True Capability (r = {correlation:.2f})")
    ax4.legend(loc="best")
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"Plot saved to: {save_path}")

    if show:
        plt.show()

    return fig


def plot_strategy_evolution(
    history: list[dict],
    save_path: Optional[str] = None,
    show: bool = True,
):
    """
    Plot strategy evolution as line charts.

    Args:
        history: List of round data dicts from simulation
        save_path: If provided, save figure to this path
        show: Whether to display the plot
    """
    if not history:
        print("No history to plot")
        return

    rounds = [h["round"] for h in history]
    providers = list(history[0]["scores"].keys())
    colors = {providers[0]: "#E63946", providers[1]: "#457B9D"}

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle("Strategy Evolution", fontsize=12, fontweight="bold")

    # R&D Investment
    ax1 = axes[0]
    for provider in providers:
        rnd = [h["strategies"][provider]["rnd"] for h in history]
        ax1.plot(rounds, rnd, "o-", label=provider, color=colors[provider],
                 markersize=4, linewidth=2)
    ax1.set_xlabel("Round")
    ax1.set_ylabel("R&D Investment")
    ax1.set_title("R&D Investment Over Time")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1)
    ax1.axhline(y=0.5, color="gray", linestyle=":", alpha=0.5)

    # Gaming Investment
    ax2 = axes[1]
    for provider in providers:
        gaming = [h["strategies"][provider]["gaming"] for h in history]
        ax2.plot(rounds, gaming, "o-", label=provider, color=colors[provider],
                 markersize=4, linewidth=2)
    ax2.set_xlabel("Round")
    ax2.set_ylabel("Gaming Investment")
    ax2.set_title("Gaming Investment Over Time")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 1)
    ax2.axhline(y=0.5, color="gray", linestyle=":", alpha=0.5)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")

    if show:
        plt.show()

    return fig


def plot_belief_accuracy(
    history: list[dict],
    save_path: Optional[str] = None,
    show: bool = True,
):
    """
    Plot how accurate providers' beliefs are about their own capability.

    Args:
        history: List of round data dicts from simulation
        save_path: If provided, save figure to this path
        show: Whether to display the plot
    """
    if not history:
        print("No history to plot")
        return

    rounds = [h["round"] for h in history]
    providers = list(history[0]["scores"].keys())
    colors = {providers[0]: "#E63946", providers[1]: "#457B9D"}

    fig, ax = plt.subplots(figsize=(10, 5))

    for provider in providers:
        true_caps = np.array([h["true_capabilities"][provider] for h in history])
        believed_caps = np.array([h["believed_capabilities"][provider] for h in history])
        belief_error = believed_caps - true_caps

        ax.plot(rounds, belief_error, "o-", label=provider, color=colors[provider],
                markersize=4, linewidth=2)

    ax.axhline(y=0, color="black", linestyle="-", linewidth=1, alpha=0.5)
    ax.fill_between(rounds, -0.05, 0.05, alpha=0.1, color="green", label="Accurate zone")

    ax.set_xlabel("Round")
    ax.set_ylabel("Belief Error (Believed - True)")
    ax.set_title("Belief Accuracy: How Well Do Providers Know Their Own Capability?")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")

    if show:
        plt.show()

    return fig


def plot_validity_over_time(
    history: list[dict],
    window_size: int = 5,
    save_path: Optional[str] = None,
    show: bool = True,
):
    """
    Plot rolling correlation between scores and true capability over time.

    This shows how benchmark validity degrades (or not) as the simulation progresses.

    Args:
        history: List of round data dicts from simulation
        window_size: Number of rounds to use for rolling correlation
        save_path: If provided, save figure to this path
        show: Whether to display the plot
    """
    if len(history) < window_size:
        print(f"Need at least {window_size} rounds for rolling correlation")
        return

    providers = list(history[0]["scores"].keys())

    # Compute rolling correlation
    correlations = []
    rounds_used = []

    for i in range(window_size, len(history) + 1):
        window = history[i-window_size:i]

        all_scores = []
        all_caps = []
        for h in window:
            for provider in providers:
                all_scores.append(h["scores"][provider])
                all_caps.append(h["true_capabilities"][provider])

        if len(all_scores) >= 2:
            corr = np.corrcoef(all_scores, all_caps)[0, 1]
            correlations.append(corr)
            rounds_used.append(i - 1)

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(rounds_used, correlations, "o-", color="#2A9D8F", markersize=5, linewidth=2)
    ax.axhline(y=0.7, color="green", linestyle="--", alpha=0.5, label="Good validity (0.7)")
    ax.axhline(y=0.5, color="orange", linestyle="--", alpha=0.5, label="Moderate validity (0.5)")
    ax.axhline(y=0.3, color="red", linestyle="--", alpha=0.5, label="Poor validity (0.3)")

    ax.set_xlabel("Round")
    ax.set_ylabel(f"Rolling Correlation (window={window_size})")
    ax.set_title("Benchmark Validity Over Time\n(Correlation between Scores and True Capability)")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-0.2, 1.0)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")

    if show:
        plt.show()

    return fig


def plot_consumer_satisfaction(
    history: list[dict],
    save_path: Optional[str] = None,
    show: bool = True,
):
    """
    Plot consumer satisfaction over time.

    Args:
        history: List of round data dicts from simulation
        save_path: If provided, save figure to this path
        show: Whether to display the plot
    """
    # Check if consumer data exists
    consumer_rounds = [h for h in history if "consumer_data" in h]
    if not consumer_rounds:
        print("No consumer data to plot")
        return None

    rounds = [h["round"] for h in consumer_rounds]
    avg_satisfaction = [
        h["consumer_data"].get("avg_satisfaction", 0)
        for h in consumer_rounds
    ]
    switches = [
        h["consumer_data"].get("switches", 0)
        for h in consumer_rounds
    ]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle("Consumer Dynamics", fontsize=12, fontweight="bold")

    # Satisfaction over time
    ax1 = axes[0]
    ax1.plot(rounds, avg_satisfaction, "o-", color="#2A9D8F", markersize=4, linewidth=2)
    ax1.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5, label="Neutral (0.5)")
    ax1.fill_between(rounds, 0.7, 1.0, alpha=0.1, color="green", label="High satisfaction")
    ax1.fill_between(rounds, 0, 0.3, alpha=0.1, color="red", label="Low satisfaction")
    ax1.set_xlabel("Round")
    ax1.set_ylabel("Average Consumer Satisfaction")
    ax1.set_title("Consumer Satisfaction Over Time")
    ax1.legend(loc="best", fontsize=8)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1)

    # Subscription switches
    ax2 = axes[1]
    ax2.bar(rounds, switches, color="#E76F51", alpha=0.7)
    ax2.set_xlabel("Round")
    ax2.set_ylabel("Number of Subscription Switches")
    ax2.set_title("Consumer Subscription Changes")
    ax2.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")

    if show:
        plt.show()

    return fig


def plot_policymaker_interventions(
    history: list[dict],
    save_path: Optional[str] = None,
    show: bool = True,
):
    """
    Plot policymaker interventions alongside ecosystem health metrics.

    Args:
        history: List of round data dicts from simulation
        save_path: If provided, save figure to this path
        show: Whether to display the plot
    """
    # Check if policymaker data exists
    policymaker_rounds = [h for h in history if "policymaker_data" in h]
    if not policymaker_rounds:
        print("No policymaker data to plot")
        return None

    rounds = [h["round"] for h in history]

    # Extract intervention rounds
    intervention_rounds = []
    for h in history:
        if "policymaker_data" in h:
            if h["policymaker_data"].get("interventions"):
                intervention_rounds.append(h["round"])

    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot validity correlation if available
    validity_data = []
    for i in range(5, len(history) + 1):
        window = history[i-5:i]
        providers = list(history[0]["scores"].keys())

        all_scores = []
        all_caps = []
        for h in window:
            for provider in providers:
                all_scores.append(h["scores"][provider])
                all_caps.append(h["true_capabilities"][provider])

        if len(all_scores) >= 2:
            corr = np.corrcoef(all_scores, all_caps)[0, 1]
            validity_data.append((i - 1, corr))

    if validity_data:
        validity_rounds = [v[0] for v in validity_data]
        validity_values = [v[1] for v in validity_data]
        ax.plot(validity_rounds, validity_values, "o-", color="#457B9D",
                markersize=4, linewidth=2, label="Validity Correlation")

    # Mark intervention rounds
    for ir in intervention_rounds:
        ax.axvline(x=ir, color="#E63946", linestyle="--", alpha=0.7)
    if intervention_rounds:
        ax.axvline(x=intervention_rounds[0], color="#E63946", linestyle="--",
                   alpha=0.7, label="Regulatory Intervention")

    # Add threshold lines
    ax.axhline(y=0.7, color="green", linestyle=":", alpha=0.5, label="Good validity")
    ax.axhline(y=0.5, color="orange", linestyle=":", alpha=0.5, label="Moderate validity")
    ax.axhline(y=0.3, color="red", linestyle=":", alpha=0.5, label="Poor validity")

    ax.set_xlabel("Round")
    ax.set_ylabel("Validity Correlation")
    ax.set_title("Benchmark Validity and Regulatory Interventions")
    ax.legend(loc="best", fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-0.2, 1.0)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")

    if show:
        plt.show()

    return fig


def plot_ecosystem_dashboard(
    history: list[dict],
    save_path: Optional[str] = None,
    show: bool = True,
):
    """
    Create a comprehensive dashboard showing all ecosystem dynamics.

    Args:
        history: List of round data dicts from simulation
        save_path: If provided, save figure to this path
        show: Whether to display the plot
    """
    if not history:
        print("No history to plot")
        return None

    has_consumers = any("consumer_data" in h for h in history)
    has_policymakers = any("policymaker_data" in h for h in history)

    # Determine subplot layout
    n_rows = 2
    if has_consumers or has_policymakers:
        n_rows = 3

    fig, axes = plt.subplots(n_rows, 2, figsize=(14, 4 * n_rows))
    fig.suptitle("Evaluation Ecosystem Dashboard", fontsize=14, fontweight="bold")

    rounds = [h["round"] for h in history]
    providers = list(history[0]["scores"].keys())
    colors = {providers[0]: "#E63946", providers[1]: "#457B9D"}

    # Row 1: Scores and Capability
    # Plot 1: Scores over time
    ax1 = axes[0, 0]
    for provider in providers:
        scores = [h["scores"][provider] for h in history]
        ax1.plot(rounds, scores, "o-", label=provider, color=colors[provider],
                 markersize=4, linewidth=1.5, alpha=0.8)
    ax1.set_xlabel("Round")
    ax1.set_ylabel("Benchmark Score")
    ax1.set_title("Benchmark Scores Over Time")
    ax1.legend(loc="best")
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1)

    # Plot 2: True vs Believed Capability
    ax2 = axes[0, 1]
    for provider in providers:
        true_caps = [h["true_capabilities"][provider] for h in history]
        believed_caps = [h["believed_capabilities"][provider] for h in history]
        ax2.plot(rounds, true_caps, "-", label=f"{provider} (true)",
                 color=colors[provider], linewidth=2)
        ax2.plot(rounds, believed_caps, "--", label=f"{provider} (believed)",
                 color=colors[provider], linewidth=1.5, alpha=0.7)
    ax2.set_xlabel("Round")
    ax2.set_ylabel("Capability")
    ax2.set_title("True vs Believed Capability")
    ax2.legend(loc="best", fontsize=8)
    ax2.grid(True, alpha=0.3)

    # Row 2: Strategy and Validity
    # Plot 3: Gaming investment
    ax3 = axes[1, 0]
    for provider in providers:
        gaming = [h["strategies"][provider]["gaming"] for h in history]
        ax3.plot(rounds, gaming, "o-", label=provider, color=colors[provider],
                 markersize=4, linewidth=2)
    ax3.axhline(y=0.5, color="gray", linestyle=":", alpha=0.5)
    ax3.set_xlabel("Round")
    ax3.set_ylabel("Gaming Investment")
    ax3.set_title("Gaming Investment Over Time")
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(0, 1)

    # Plot 4: Validity correlation
    ax4 = axes[1, 1]
    validity_data = []
    for i in range(5, len(history) + 1):
        window = history[i-5:i]
        all_scores = []
        all_caps = []
        for h in window:
            for provider in providers:
                all_scores.append(h["scores"][provider])
                all_caps.append(h["true_capabilities"][provider])
        if len(all_scores) >= 2:
            corr = np.corrcoef(all_scores, all_caps)[0, 1]
            validity_data.append((i - 1, corr))

    if validity_data:
        validity_rounds = [v[0] for v in validity_data]
        validity_values = [v[1] for v in validity_data]
        ax4.plot(validity_rounds, validity_values, "o-", color="#2A9D8F",
                 markersize=5, linewidth=2)
        ax4.axhline(y=0.7, color="green", linestyle="--", alpha=0.5)
        ax4.axhline(y=0.5, color="orange", linestyle="--", alpha=0.5)
        ax4.axhline(y=0.3, color="red", linestyle="--", alpha=0.5)
    ax4.set_xlabel("Round")
    ax4.set_ylabel("Validity Correlation")
    ax4.set_title("Benchmark Validity Over Time")
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(-0.2, 1.0)

    # Row 3: Consumer and Policymaker (if present)
    if n_rows == 3:
        # Plot 5: Consumer satisfaction
        ax5 = axes[2, 0]
        if has_consumers:
            consumer_rounds = [h["round"] for h in history if "consumer_data" in h]
            avg_satisfaction = [
                h["consumer_data"].get("avg_satisfaction", 0)
                for h in history if "consumer_data" in h
            ]
            if consumer_rounds and avg_satisfaction:
                ax5.plot(consumer_rounds, avg_satisfaction, "o-", color="#2A9D8F",
                         markersize=4, linewidth=2)
                ax5.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5)
                ax5.fill_between(consumer_rounds, 0.7, 1.0, alpha=0.1, color="green")
                ax5.fill_between(consumer_rounds, 0, 0.3, alpha=0.1, color="red")
        ax5.set_xlabel("Round")
        ax5.set_ylabel("Average Satisfaction")
        ax5.set_title("Consumer Satisfaction")
        ax5.grid(True, alpha=0.3)
        ax5.set_ylim(0, 1)

        # Plot 6: Policymaker interventions
        ax6 = axes[2, 1]
        if has_policymakers:
            intervention_rounds = []
            for h in history:
                if "policymaker_data" in h and h["policymaker_data"].get("interventions"):
                    intervention_rounds.append(h["round"])

            # Create a simple timeline
            intervention_indicator = [
                1 if r in intervention_rounds else 0 for r in rounds
            ]
            ax6.bar(rounds, intervention_indicator, color="#E63946", alpha=0.7)
            ax6.set_ylabel("Intervention (1=Yes)")
        ax6.set_xlabel("Round")
        ax6.set_title("Regulatory Interventions")
        ax6.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")

    if show:
        plt.show()

    return fig


def create_all_plots(
    history: list[dict],
    output_dir: str = "./plots",
    show: bool = True,
):
    """
    Create and save all plots.

    Args:
        history: List of round data dicts from simulation
        output_dir: Directory to save plots
        show: Whether to display plots
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    print("Creating plots...")

    plot_simulation_results(
        history,
        save_path=f"{output_dir}/simulation_overview.png",
        show=show
    )

    plot_strategy_evolution(
        history,
        save_path=f"{output_dir}/strategy_evolution.png",
        show=show
    )

    plot_belief_accuracy(
        history,
        save_path=f"{output_dir}/belief_accuracy.png",
        show=show
    )

    if len(history) >= 5:
        plot_validity_over_time(
            history,
            save_path=f"{output_dir}/validity_over_time.png",
            show=show
        )

    # New plots for consumer and policymaker
    if any("consumer_data" in h for h in history):
        fig = plot_consumer_satisfaction(history, show=False)
        if fig:
            fig.savefig(f"{output_dir}/consumer_satisfaction.png", dpi=150, bbox_inches="tight")
            plt.close(fig)

    if any("policymaker_data" in h for h in history):
        fig = plot_policymaker_interventions(history, show=False)
        if fig:
            fig.savefig(f"{output_dir}/policymaker_interventions.png", dpi=150, bbox_inches="tight")
            plt.close(fig)

    # Create comprehensive dashboard
    fig = plot_ecosystem_dashboard(history, show=False)
    if fig:
        fig.savefig(f"{output_dir}/ecosystem_dashboard.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    print(f"All plots saved to: {output_dir}")


if __name__ == "__main__":
    # Run simulation and create plots
    from simulation import run_default_simulation

    sim = run_default_simulation()
    create_all_plots(sim.history, show=True)
