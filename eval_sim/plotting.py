"""
Plotting utilities for Evaluation Ecosystem Simulation

Provides dashboards for each actor type and a summary dashboard.
Scalable to N providers/actors.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from typing import Optional


# =============================================================================
# Color Palettes and Styling
# =============================================================================

def get_provider_colors(n_providers: int) -> list:
    """Get a color palette that scales to N providers."""
    # Use a colorblind-friendly palette
    base_colors = [
        "#E63946",  # Red
        "#457B9D",  # Blue
        "#2A9D8F",  # Teal
        "#E9C46A",  # Yellow
        "#F4A261",  # Orange
        "#9C6644",  # Brown
        "#6A4C93",  # Purple
        "#1D3557",  # Dark Blue
    ]
    if n_providers <= len(base_colors):
        return base_colors[:n_providers]
    # If more providers, use a colormap
    cmap = plt.cm.get_cmap('tab20')
    return [cmap(i / n_providers) for i in range(n_providers)]


def get_investment_colors() -> dict:
    """Colors for the 4-way investment portfolio."""
    return {
        "fundamental_research": "#2E86AB",    # Blue
        "training_optimization": "#A23B72",   # Magenta
        "evaluation_engineering": "#F18F01",  # Orange
        "safety_alignment": "#C73E1D",        # Red
    }


def style_axis(ax, title: str, xlabel: str, ylabel: str, legend: bool = True):
    """Apply consistent styling to an axis."""
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.grid(True, alpha=0.3)
    if legend:
        ax.legend(loc='best', fontsize=8)


# =============================================================================
# Data Extraction Helpers
# =============================================================================

def get_providers(history: list) -> list:
    """Extract provider names from history."""
    if not history:
        return []
    return list(history[0]["scores"].keys())


def get_strategy_key(history: list) -> str:
    """Determine which strategy format is used."""
    if not history:
        return "new"
    first_strategy = list(history[0]["strategies"].values())[0]
    if "fundamental_research" in first_strategy:
        return "new"
    return "old"


def extract_investment(history: list, provider: str, investment_type: str) -> list:
    """Extract investment values for a provider over time."""
    return [h["strategies"][provider].get(investment_type, 0) for h in history]


def compute_rolling_correlation(history: list, window_size: int = 5) -> tuple:
    """Compute rolling correlation between scores and true capabilities."""
    if len(history) < window_size:
        return [], []

    providers = get_providers(history)
    correlations = []
    rounds_used = []

    for i in range(window_size, len(history) + 1):
        window = history[i - window_size:i]
        all_scores = []
        all_caps = []
        for h in window:
            for provider in providers:
                all_scores.append(h["scores"][provider])
                all_caps.append(h["true_capabilities"][provider])

        if len(all_scores) >= 2:
            corr = np.corrcoef(all_scores, all_caps)[0, 1]
            if not np.isnan(corr):
                correlations.append(corr)
                rounds_used.append(i - 1)

    return rounds_used, correlations


# =============================================================================
# Provider Dashboard
# =============================================================================

def plot_provider_dashboard(
    history: list,
    save_path: Optional[str] = None,
    show: bool = True,
    figsize: tuple = (16, 12),
) -> Optional[plt.Figure]:
    """
    Create a comprehensive dashboard for Model Providers.

    Panels:
    1. Benchmark Scores over time
    2. True vs Believed Capability
    3. Investment Portfolio (stacked area)
    4. Evaluation Engineering trend (gaming metric)
    5. Score - True Capability Gap
    6. Capability Growth comparison

    Args:
        history: List of round data dicts
        save_path: Path to save figure
        show: Whether to display
        figsize: Figure size

    Returns:
        matplotlib Figure or None
    """
    if not history:
        print("No history to plot")
        return None

    providers = get_providers(history)
    n_providers = len(providers)
    colors = get_provider_colors(n_providers)
    provider_colors = {p: colors[i] for i, p in enumerate(providers)}
    inv_colors = get_investment_colors()

    rounds = [h["round"] for h in history]

    fig, axes = plt.subplots(2, 3, figsize=figsize)
    fig.suptitle("Provider Dashboard", fontsize=14, fontweight='bold')

    # --- Panel 1: Scores over time ---
    ax1 = axes[0, 0]
    for provider in providers:
        scores = [h["scores"][provider] for h in history]
        ax1.plot(rounds, scores, 'o-', label=provider, color=provider_colors[provider],
                 markersize=3, linewidth=1.5, alpha=0.8)
    ax1.set_ylim(0, 1)
    style_axis(ax1, "Benchmark Scores Over Time", "Round", "Score")

    # --- Panel 2: True vs Believed Capability ---
    ax2 = axes[0, 1]
    for provider in providers:
        true_caps = [h["true_capabilities"][provider] for h in history]
        believed_caps = [h["believed_capabilities"][provider] for h in history]
        ax2.plot(rounds, true_caps, '-', label=f"{provider} (true)",
                 color=provider_colors[provider], linewidth=2)
        ax2.plot(rounds, believed_caps, '--', label=f"{provider} (believed)",
                 color=provider_colors[provider], linewidth=1.5, alpha=0.6)
    style_axis(ax2, "True vs Believed Capability", "Round", "Capability")

    # --- Panel 3: Investment Portfolio (stacked area for first provider, lines for comparison) ---
    ax3 = axes[0, 2]
    investment_types = ["fundamental_research", "training_optimization",
                        "evaluation_engineering", "safety_alignment"]

    # Show stacked area for visual clarity of one provider
    if n_providers >= 1:
        provider = providers[0]
        bottom = np.zeros(len(rounds))
        for inv_type in investment_types:
            values = np.array(extract_investment(history, provider, inv_type))
            ax3.fill_between(rounds, bottom, bottom + values,
                            alpha=0.7, label=inv_type.replace("_", " ").title(),
                            color=inv_colors[inv_type])
            bottom += values
        ax3.set_title(f"Investment Portfolio ({provider})", fontsize=11, fontweight='bold')
    ax3.set_ylim(0, 1.05)
    ax3.set_xlabel("Round", fontsize=9)
    ax3.set_ylabel("Allocation", fontsize=9)
    ax3.legend(loc='upper right', fontsize=7)
    ax3.grid(True, alpha=0.3)

    # --- Panel 4: Evaluation Engineering (Gaming) Over Time ---
    ax4 = axes[1, 0]
    for provider in providers:
        eval_eng = extract_investment(history, provider, "evaluation_engineering")
        ax4.plot(rounds, eval_eng, 'o-', label=provider, color=provider_colors[provider],
                 markersize=3, linewidth=2)
    ax4.axhline(y=0.25, color='gray', linestyle=':', alpha=0.5, label='Balanced (0.25)')
    ax4.set_ylim(0, 1)
    style_axis(ax4, "Evaluation Engineering (Gaming) Over Time", "Round", "Investment")

    # --- Panel 5: Score - Capability Gap ---
    ax5 = axes[1, 1]
    for provider in providers:
        scores = np.array([h["scores"][provider] for h in history])
        true_caps = np.array([h["true_capabilities"][provider] for h in history])
        gap = scores - true_caps
        ax5.plot(rounds, gap, 'o-', label=provider, color=provider_colors[provider],
                 markersize=3, linewidth=2)
    ax5.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    ax5.fill_between(rounds, 0, 0.1, alpha=0.1, color='orange', label='Inflated')
    ax5.fill_between(rounds, -0.1, 0, alpha=0.1, color='blue', label='Deflated')
    style_axis(ax5, "Score - True Capability Gap", "Round", "Gap (Score - True)")

    # --- Panel 6: Capability Growth Bar Chart ---
    ax6 = axes[1, 2]
    initial_caps = [history[0]["true_capabilities"][p] for p in providers]
    final_caps = [history[-1]["true_capabilities"][p] for p in providers]
    growth = [f - i for i, f in zip(initial_caps, final_caps)]

    x = np.arange(len(providers))
    bars = ax6.bar(x, growth, color=[provider_colors[p] for p in providers], alpha=0.8)
    ax6.set_xticks(x)
    ax6.set_xticklabels(providers, rotation=45, ha='right', fontsize=8)
    ax6.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    style_axis(ax6, "Capability Growth (Final - Initial)", "", "Growth", legend=False)

    # Add value labels on bars
    for bar, val in zip(bars, growth):
        ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                f'{val:.3f}', ha='center', va='bottom', fontsize=8)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Provider dashboard saved to: {save_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


# =============================================================================
# Consumer Dashboard
# =============================================================================

def plot_consumer_dashboard(
    history: list,
    save_path: Optional[str] = None,
    show: bool = True,
    figsize: tuple = (14, 10),
) -> Optional[plt.Figure]:
    """
    Create a dashboard for Consumer actors.

    Panels:
    1. Average Satisfaction over time
    2. Subscription Switches per round
    3. Market Share (subscriptions per provider)
    4. Satisfaction Distribution (min/max/avg)

    Args:
        history: List of round data dicts
        save_path: Path to save figure
        show: Whether to display
        figsize: Figure size

    Returns:
        matplotlib Figure or None
    """
    consumer_rounds = [h for h in history if "consumer_data" in h]
    if not consumer_rounds:
        print("No consumer data to plot")
        return None

    providers = get_providers(history)
    provider_colors = {p: c for p, c in zip(providers, get_provider_colors(len(providers)))}

    rounds = [h["round"] for h in consumer_rounds]

    fig, axes = plt.subplots(2, 2, figsize=figsize)
    fig.suptitle("Consumer Dashboard", fontsize=14, fontweight='bold')

    # --- Panel 1: Average Satisfaction ---
    ax1 = axes[0, 0]
    avg_satisfaction = [h["consumer_data"].get("avg_satisfaction", 0) for h in consumer_rounds]
    ax1.plot(rounds, avg_satisfaction, 'o-', color='#2A9D8F', markersize=4, linewidth=2)
    ax1.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='Neutral')
    ax1.fill_between(rounds, 0.7, 1.0, alpha=0.1, color='green', label='High')
    ax1.fill_between(rounds, 0, 0.3, alpha=0.1, color='red', label='Low')
    ax1.set_ylim(0, 1)
    style_axis(ax1, "Average Consumer Satisfaction", "Round", "Satisfaction")

    # --- Panel 2: Subscription Switches ---
    ax2 = axes[0, 1]
    switches = [h["consumer_data"].get("switches", 0) for h in consumer_rounds]
    ax2.bar(rounds, switches, color='#E76F51', alpha=0.7)
    ax2.set_ylabel("Switches", fontsize=9)
    style_axis(ax2, "Subscription Switches Per Round", "Round", "Switches", legend=False)

    # --- Panel 3: Market Share Over Time ---
    ax3 = axes[1, 0]

    # Count subscriptions per provider per round
    market_share = {p: [] for p in providers}
    for h in consumer_rounds:
        subs = h["consumer_data"].get("subscriptions", {})
        counts = {p: 0 for p in providers}
        for consumer, provider in subs.items():
            if provider in counts:
                counts[provider] += 1
        for p in providers:
            market_share[p].append(counts[p])

    # Stacked area chart
    bottom = np.zeros(len(rounds))
    for provider in providers:
        values = np.array(market_share[provider])
        ax3.fill_between(rounds, bottom, bottom + values,
                        alpha=0.7, label=provider, color=provider_colors[provider])
        bottom += values

    style_axis(ax3, "Market Share (Subscriptions)", "Round", "Number of Consumers")

    # --- Panel 4: Satisfaction Range (min/max/avg) ---
    ax4 = axes[1, 1]

    min_sats = []
    max_sats = []
    for h in consumer_rounds:
        sat_dict = h["consumer_data"].get("satisfaction", {})
        if sat_dict:
            vals = list(sat_dict.values())
            min_sats.append(min(vals))
            max_sats.append(max(vals))
        else:
            min_sats.append(h["consumer_data"].get("min_satisfaction", 0))
            max_sats.append(h["consumer_data"].get("avg_satisfaction", 0))

    ax4.fill_between(rounds, min_sats, max_sats, alpha=0.3, color='#457B9D', label='Range')
    ax4.plot(rounds, avg_satisfaction, 'o-', color='#457B9D', markersize=3,
             linewidth=2, label='Average')
    ax4.set_ylim(0, 1)
    style_axis(ax4, "Satisfaction Range", "Round", "Satisfaction")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Consumer dashboard saved to: {save_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


# =============================================================================
# Policymaker Dashboard
# =============================================================================

def plot_policymaker_dashboard(
    history: list,
    save_path: Optional[str] = None,
    show: bool = True,
    figsize: tuple = (14, 8),
) -> Optional[plt.Figure]:
    """
    Create a dashboard for Policymaker actors.

    Panels:
    1. Validity Correlation with Intervention Markers
    2. Intervention Timeline
    3. Active Regulations Count
    4. Intervention Types Distribution

    Args:
        history: List of round data dicts
        save_path: Path to save figure
        show: Whether to display
        figsize: Figure size

    Returns:
        matplotlib Figure or None
    """
    policymaker_rounds = [h for h in history if "policymaker_data" in h]
    if not policymaker_rounds:
        print("No policymaker data to plot")
        return None

    rounds = [h["round"] for h in history]

    # Extract intervention data
    intervention_rounds = []
    intervention_types = []
    for h in history:
        if "policymaker_data" in h:
            interventions = h["policymaker_data"].get("interventions", [])
            if interventions:
                intervention_rounds.append(h["round"])
                for interv in interventions:
                    if "type" in interv:
                        intervention_types.append(interv["type"])

    fig, axes = plt.subplots(2, 2, figsize=figsize)
    fig.suptitle("Policymaker Dashboard", fontsize=14, fontweight='bold')

    # --- Panel 1: Validity Correlation with Interventions ---
    ax1 = axes[0, 0]
    validity_rounds, validity_values = compute_rolling_correlation(history)

    if validity_values:
        ax1.plot(validity_rounds, validity_values, 'o-', color='#457B9D',
                 markersize=4, linewidth=2, label='Validity')

    # Mark interventions
    for ir in intervention_rounds:
        ax1.axvline(x=ir, color='#E63946', linestyle='--', alpha=0.7)
    if intervention_rounds:
        ax1.axvline(x=intervention_rounds[0], color='#E63946', linestyle='--',
                   alpha=0.7, label='Intervention')

    ax1.axhline(y=0.7, color='green', linestyle=':', alpha=0.5)
    ax1.axhline(y=0.5, color='orange', linestyle=':', alpha=0.5)
    ax1.axhline(y=0.3, color='red', linestyle=':', alpha=0.5)
    ax1.set_ylim(-0.2, 1.0)
    style_axis(ax1, "Benchmark Validity & Interventions", "Round", "Correlation")

    # --- Panel 2: Intervention Timeline ---
    ax2 = axes[0, 1]
    intervention_indicator = [1 if r in intervention_rounds else 0 for r in rounds]
    colors = ['#E63946' if v else '#CCCCCC' for v in intervention_indicator]
    ax2.bar(rounds, [1]*len(rounds), color=colors, alpha=0.7)
    ax2.set_ylim(0, 1.5)
    ax2.set_yticks([])
    style_axis(ax2, "Intervention Timeline", "Round", "", legend=False)

    # Add count annotation
    total_interventions = sum(intervention_indicator)
    ax2.text(0.95, 0.95, f"Total: {total_interventions}", transform=ax2.transAxes,
             ha='right', va='top', fontsize=10, fontweight='bold')

    # --- Panel 3: Active Regulations Count ---
    ax3 = axes[1, 0]
    active_counts = []
    for h in history:
        if "policymaker_data" in h:
            active = h["policymaker_data"].get("active_regulations", [])
            active_counts.append(len(active))
        else:
            active_counts.append(0)

    ax3.fill_between(rounds, 0, active_counts, alpha=0.5, color='#6A4C93')
    ax3.plot(rounds, active_counts, 'o-', color='#6A4C93', markersize=3, linewidth=2)
    style_axis(ax3, "Active Regulations Over Time", "Round", "Count", legend=False)

    # --- Panel 4: Intervention Types Distribution ---
    ax4 = axes[1, 1]
    if intervention_types:
        unique_types = list(set(intervention_types))
        type_counts = [intervention_types.count(t) for t in unique_types]
        colors = plt.cm.Set2(np.linspace(0, 1, len(unique_types)))
        ax4.pie(type_counts, labels=unique_types, autopct='%1.0f%%', colors=colors,
                textprops={'fontsize': 9})
        ax4.set_title("Intervention Types", fontsize=11, fontweight='bold')
    else:
        ax4.text(0.5, 0.5, "No interventions", ha='center', va='center', fontsize=12)
        ax4.set_title("Intervention Types", fontsize=11, fontweight='bold')
        ax4.axis('off')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Policymaker dashboard saved to: {save_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


# =============================================================================
# Evaluator Dashboard
# =============================================================================

def plot_evaluator_dashboard(
    history: list,
    save_path: Optional[str] = None,
    show: bool = True,
    figsize: tuple = (14, 10),
) -> Optional[plt.Figure]:
    """
    Create a dashboard for the Evaluator (benchmark analysis).

    Panels:
    1. Overall Validity Correlation Over Time
    2. Score vs True Capability Scatter
    3. Per-Benchmark Scores (if multi-benchmark)
    4. Score Distribution by Provider

    Args:
        history: List of round data dicts
        save_path: Path to save figure
        show: Whether to display
        figsize: Figure size

    Returns:
        matplotlib Figure or None
    """
    if not history:
        print("No history to plot")
        return None

    providers = get_providers(history)
    provider_colors = {p: c for p, c in zip(providers, get_provider_colors(len(providers)))}
    rounds = [h["round"] for h in history]

    has_multi_benchmark = "per_benchmark_scores" in history[0]

    fig, axes = plt.subplots(2, 2, figsize=figsize)
    fig.suptitle("Evaluator Dashboard (Benchmark Analysis)", fontsize=14, fontweight='bold')

    # --- Panel 1: Validity Correlation Over Time ---
    ax1 = axes[0, 0]
    validity_rounds, validity_values = compute_rolling_correlation(history)

    if validity_values:
        ax1.plot(validity_rounds, validity_values, 'o-', color='#2A9D8F',
                 markersize=5, linewidth=2)
        ax1.axhline(y=0.7, color='green', linestyle='--', alpha=0.5, label='Good (0.7)')
        ax1.axhline(y=0.5, color='orange', linestyle='--', alpha=0.5, label='Moderate (0.5)')
        ax1.axhline(y=0.3, color='red', linestyle='--', alpha=0.5, label='Poor (0.3)')
    ax1.set_ylim(-0.2, 1.0)
    style_axis(ax1, "Benchmark Validity Over Time", "Round", "Correlation (Score vs True)")

    # --- Panel 2: Score vs True Capability Scatter ---
    ax2 = axes[0, 1]
    for provider in providers:
        scores = [h["scores"][provider] for h in history]
        true_caps = [h["true_capabilities"][provider] for h in history]
        ax2.scatter(true_caps, scores, label=provider, color=provider_colors[provider],
                   alpha=0.6, s=30)

    # Perfect validity line
    all_vals = []
    for provider in providers:
        all_vals.extend([h["scores"][provider] for h in history])
        all_vals.extend([h["true_capabilities"][provider] for h in history])
    if all_vals:
        min_val, max_val = min(all_vals), max(all_vals)
        ax2.plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.3,
                 label='Perfect Validity')

    # Compute overall correlation
    all_scores, all_caps = [], []
    for provider in providers:
        all_scores.extend([h["scores"][provider] for h in history])
        all_caps.extend([h["true_capabilities"][provider] for h in history])
    if len(all_scores) >= 2:
        corr = np.corrcoef(all_scores, all_caps)[0, 1]
        ax2.set_title(f"Score vs True Capability (r = {corr:.2f})", fontsize=11, fontweight='bold')
    else:
        ax2.set_title("Score vs True Capability", fontsize=11, fontweight='bold')
    ax2.set_xlabel("True Capability", fontsize=9)
    ax2.set_ylabel("Benchmark Score", fontsize=9)
    ax2.legend(loc='best', fontsize=8)
    ax2.grid(True, alpha=0.3)

    # --- Panel 3: Per-Benchmark Scores or Score Trends ---
    ax3 = axes[1, 0]
    if has_multi_benchmark:
        benchmark_names = history[0].get("benchmark_names", [])
        bench_colors = get_provider_colors(len(benchmark_names))

        # Plot average score per benchmark over time
        for i, bench_name in enumerate(benchmark_names):
            bench_avgs = []
            for h in history:
                bench_scores = h["per_benchmark_scores"].get(bench_name, {})
                if bench_scores:
                    bench_avgs.append(np.mean(list(bench_scores.values())))
                else:
                    bench_avgs.append(0)
            ax3.plot(rounds, bench_avgs, 'o-', label=bench_name, color=bench_colors[i],
                    markersize=3, linewidth=2)
        style_axis(ax3, "Average Score by Benchmark", "Round", "Score")
    else:
        # Single benchmark - show score trends
        for provider in providers:
            scores = [h["scores"][provider] for h in history]
            ax3.plot(rounds, scores, 'o-', label=provider, color=provider_colors[provider],
                    markersize=3, linewidth=1.5)
        ax3.set_ylim(0, 1)
        style_axis(ax3, "Score Trends", "Round", "Score")

    # --- Panel 4: Score Distribution Box Plot ---
    ax4 = axes[1, 1]
    score_data = []
    for provider in providers:
        scores = [h["scores"][provider] for h in history]
        score_data.append(scores)

    bp = ax4.boxplot(score_data, labels=providers, patch_artist=True)
    for patch, provider in zip(bp['boxes'], providers):
        patch.set_facecolor(provider_colors[provider])
        patch.set_alpha(0.7)
    ax4.set_xticklabels(providers, rotation=45, ha='right', fontsize=8)
    style_axis(ax4, "Score Distribution by Provider", "", "Score", legend=False)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Evaluator dashboard saved to: {save_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


# =============================================================================
# Summary Dashboard
# =============================================================================

def plot_summary_dashboard(
    history: list,
    save_path: Optional[str] = None,
    show: bool = True,
    figsize: tuple = (18, 12),
) -> Optional[plt.Figure]:
    """
    Create a comprehensive summary dashboard showing all ecosystem dynamics.

    Layout (3x3):
    Row 1: Scores | True vs Believed | Investment Portfolio
    Row 2: Eval Engineering | Validity | Score-Capability Gap
    Row 3: Consumer Satisfaction | Market Share | Interventions

    Args:
        history: List of round data dicts
        save_path: Path to save figure
        show: Whether to display
        figsize: Figure size

    Returns:
        matplotlib Figure or None
    """
    if not history:
        print("No history to plot")
        return None

    providers = get_providers(history)
    n_providers = len(providers)
    colors = get_provider_colors(n_providers)
    provider_colors = {p: colors[i] for i, p in enumerate(providers)}
    inv_colors = get_investment_colors()

    rounds = [h["round"] for h in history]
    has_consumers = any("consumer_data" in h for h in history)
    has_policymakers = any("policymaker_data" in h for h in history)

    fig, axes = plt.subplots(3, 3, figsize=figsize)
    fig.suptitle("Evaluation Ecosystem Summary Dashboard", fontsize=16, fontweight='bold')

    # =========== ROW 1 ===========

    # --- Panel 1,1: Scores Over Time ---
    ax = axes[0, 0]
    for provider in providers:
        scores = [h["scores"][provider] for h in history]
        ax.plot(rounds, scores, 'o-', label=provider, color=provider_colors[provider],
                markersize=3, linewidth=1.5, alpha=0.8)
    ax.set_ylim(0, 1)
    style_axis(ax, "Benchmark Scores", "Round", "Score")

    # --- Panel 1,2: True vs Believed Capability ---
    ax = axes[0, 1]
    for provider in providers:
        true_caps = [h["true_capabilities"][provider] for h in history]
        believed_caps = [h["believed_capabilities"][provider] for h in history]
        ax.plot(rounds, true_caps, '-', color=provider_colors[provider], linewidth=2)
        ax.plot(rounds, believed_caps, '--', color=provider_colors[provider],
                linewidth=1.5, alpha=0.6)
    # Custom legend
    solid_line = mpatches.Patch(color='gray', label='True')
    dashed_line = mpatches.Patch(color='gray', alpha=0.6, label='Believed')
    ax.legend(handles=[solid_line, dashed_line], loc='best', fontsize=8)
    style_axis(ax, "True vs Believed Capability", "Round", "Capability", legend=False)

    # --- Panel 1,3: Investment Portfolio (first provider) ---
    ax = axes[0, 2]
    investment_types = ["fundamental_research", "training_optimization",
                        "evaluation_engineering", "safety_alignment"]
    if providers:
        provider = providers[0]
        bottom = np.zeros(len(rounds))
        for inv_type in investment_types:
            values = np.array(extract_investment(history, provider, inv_type))
            ax.fill_between(rounds, bottom, bottom + values, alpha=0.7,
                           label=inv_type.replace("_", " ").title()[:12],
                           color=inv_colors[inv_type])
            bottom += values
    ax.set_ylim(0, 1.05)
    ax.set_title(f"Investment Portfolio ({providers[0] if providers else 'N/A'})",
                 fontsize=11, fontweight='bold')
    ax.set_xlabel("Round", fontsize=9)
    ax.legend(loc='upper right', fontsize=6)
    ax.grid(True, alpha=0.3)

    # =========== ROW 2 ===========

    # --- Panel 2,1: Evaluation Engineering ---
    ax = axes[1, 0]
    for provider in providers:
        eval_eng = extract_investment(history, provider, "evaluation_engineering")
        ax.plot(rounds, eval_eng, 'o-', label=provider, color=provider_colors[provider],
                markersize=3, linewidth=2)
    ax.axhline(y=0.25, color='gray', linestyle=':', alpha=0.5)
    ax.set_ylim(0, 1)
    style_axis(ax, "Evaluation Engineering (Gaming)", "Round", "Investment")

    # --- Panel 2,2: Validity Correlation ---
    ax = axes[1, 1]
    validity_rounds, validity_values = compute_rolling_correlation(history)
    if validity_values:
        ax.plot(validity_rounds, validity_values, 'o-', color='#2A9D8F',
                markersize=4, linewidth=2)
        ax.axhline(y=0.7, color='green', linestyle='--', alpha=0.5)
        ax.axhline(y=0.5, color='orange', linestyle='--', alpha=0.5)
        ax.axhline(y=0.3, color='red', linestyle='--', alpha=0.5)
    ax.set_ylim(-0.2, 1.0)
    style_axis(ax, "Benchmark Validity", "Round", "Correlation", legend=False)

    # --- Panel 2,3: Score - Capability Gap ---
    ax = axes[1, 2]
    for provider in providers:
        scores = np.array([h["scores"][provider] for h in history])
        true_caps = np.array([h["true_capabilities"][provider] for h in history])
        gap = scores - true_caps
        ax.plot(rounds, gap, 'o-', label=provider, color=provider_colors[provider],
                markersize=3, linewidth=2)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    style_axis(ax, "Score - Capability Gap", "Round", "Gap")

    # =========== ROW 3 ===========

    # --- Panel 3,1: Consumer Satisfaction ---
    ax = axes[2, 0]
    if has_consumers:
        consumer_rounds = [h["round"] for h in history if "consumer_data" in h]
        avg_satisfaction = [h["consumer_data"].get("avg_satisfaction", 0)
                          for h in history if "consumer_data" in h]
        if consumer_rounds:
            ax.plot(consumer_rounds, avg_satisfaction, 'o-', color='#2A9D8F',
                    markersize=4, linewidth=2)
            ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
            ax.fill_between(consumer_rounds, 0.7, 1.0, alpha=0.1, color='green')
            ax.fill_between(consumer_rounds, 0, 0.3, alpha=0.1, color='red')
    ax.set_ylim(0, 1)
    style_axis(ax, "Consumer Satisfaction", "Round", "Satisfaction", legend=False)
    if not has_consumers:
        ax.text(0.5, 0.5, "No consumer data", ha='center', va='center',
                transform=ax.transAxes, fontsize=10, alpha=0.5)

    # --- Panel 3,2: Market Share ---
    ax = axes[2, 1]
    if has_consumers:
        consumer_rounds_data = [h for h in history if "consumer_data" in h]
        if consumer_rounds_data:
            market_share = {p: [] for p in providers}
            plot_rounds = [h["round"] for h in consumer_rounds_data]
            for h in consumer_rounds_data:
                subs = h["consumer_data"].get("subscriptions", {})
                counts = {p: 0 for p in providers}
                for consumer, provider in subs.items():
                    if provider in counts:
                        counts[provider] += 1
                for p in providers:
                    market_share[p].append(counts[p])

            bottom = np.zeros(len(plot_rounds))
            for provider in providers:
                values = np.array(market_share[provider])
                ax.fill_between(plot_rounds, bottom, bottom + values, alpha=0.7,
                               label=provider, color=provider_colors[provider])
                bottom += values
    style_axis(ax, "Market Share", "Round", "Consumers")
    if not has_consumers:
        ax.text(0.5, 0.5, "No consumer data", ha='center', va='center',
                transform=ax.transAxes, fontsize=10, alpha=0.5)

    # --- Panel 3,3: Policymaker Interventions ---
    ax = axes[2, 2]
    if has_policymakers:
        intervention_rounds = []
        for h in history:
            if "policymaker_data" in h and h["policymaker_data"].get("interventions"):
                intervention_rounds.append(h["round"])

        intervention_indicator = [1 if r in intervention_rounds else 0 for r in rounds]
        colors_bar = ['#E63946' if v else '#EEEEEE' for v in intervention_indicator]
        ax.bar(rounds, [1]*len(rounds), color=colors_bar, alpha=0.7)
        ax.set_ylim(0, 1.5)
        ax.set_yticks([])
        ax.text(0.95, 0.95, f"Total: {len(intervention_rounds)}", transform=ax.transAxes,
                ha='right', va='top', fontsize=10, fontweight='bold')
    style_axis(ax, "Regulatory Interventions", "Round", "", legend=False)
    if not has_policymakers:
        ax.text(0.5, 0.5, "No policymaker data", ha='center', va='center',
                transform=ax.transAxes, fontsize=10, alpha=0.5)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Summary dashboard saved to: {save_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


# =============================================================================
# Individual Plot Functions (for backwards compatibility and flexibility)
# =============================================================================

def plot_scores_over_time(
    history: list,
    save_path: Optional[str] = None,
    show: bool = True,
) -> Optional[plt.Figure]:
    """Plot benchmark scores over time."""
    if not history:
        return None

    providers = get_providers(history)
    provider_colors = {p: c for p, c in zip(providers, get_provider_colors(len(providers)))}
    rounds = [h["round"] for h in history]

    fig, ax = plt.subplots(figsize=(10, 6))

    for provider in providers:
        scores = [h["scores"][provider] for h in history]
        ax.plot(rounds, scores, 'o-', label=provider, color=provider_colors[provider],
                markersize=4, linewidth=2)

    ax.set_ylim(0, 1)
    style_axis(ax, "Benchmark Scores Over Time", "Round", "Score")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


def plot_validity_over_time(
    history: list,
    window_size: int = 5,
    save_path: Optional[str] = None,
    show: bool = True,
) -> Optional[plt.Figure]:
    """Plot rolling validity correlation."""
    if len(history) < window_size:
        print(f"Need at least {window_size} rounds")
        return None

    validity_rounds, validity_values = compute_rolling_correlation(history, window_size)

    if not validity_values:
        return None

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(validity_rounds, validity_values, 'o-', color='#2A9D8F',
            markersize=5, linewidth=2)
    ax.axhline(y=0.7, color='green', linestyle='--', alpha=0.5, label='Good (0.7)')
    ax.axhline(y=0.5, color='orange', linestyle='--', alpha=0.5, label='Moderate (0.5)')
    ax.axhline(y=0.3, color='red', linestyle='--', alpha=0.5, label='Poor (0.3)')
    ax.set_ylim(-0.2, 1.0)

    style_axis(ax, f"Benchmark Validity Over Time (window={window_size})",
               "Round", "Correlation (Score vs True Capability)")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


def plot_investment_comparison(
    history: list,
    save_path: Optional[str] = None,
    show: bool = True,
) -> Optional[plt.Figure]:
    """Plot investment portfolio comparison across all providers."""
    if not history:
        return None

    providers = get_providers(history)
    provider_colors = {p: c for p, c in zip(providers, get_provider_colors(len(providers)))}
    inv_colors = get_investment_colors()
    investment_types = list(inv_colors.keys())

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Investment Comparison Across Providers", fontsize=14, fontweight='bold')

    rounds = [h["round"] for h in history]

    for idx, inv_type in enumerate(investment_types):
        ax = axes[idx // 2, idx % 2]
        for provider in providers:
            values = extract_investment(history, provider, inv_type)
            ax.plot(rounds, values, 'o-', label=provider, color=provider_colors[provider],
                    markersize=3, linewidth=2)
        ax.axhline(y=0.25, color='gray', linestyle=':', alpha=0.5)
        ax.set_ylim(0, 1)
        style_axis(ax, inv_type.replace("_", " ").title(), "Round", "Investment")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


# =============================================================================
# Convenience Function: Create All Dashboards
# =============================================================================

def create_all_dashboards(
    history: list,
    output_dir: str = "./plots",
    show: bool = False,
) -> dict:
    """
    Create and save all dashboards.

    Args:
        history: List of round data dicts
        output_dir: Directory to save plots
        show: Whether to display plots

    Returns:
        Dict of {dashboard_name: figure_path}
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    saved = {}

    print("Creating dashboards...")

    # Provider Dashboard
    fig = plot_provider_dashboard(history, show=False)
    if fig:
        path = f"{output_dir}/provider_dashboard.png"
        fig.savefig(path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        saved['provider_dashboard'] = path
        print(f"  - Provider dashboard saved")

    # Consumer Dashboard
    fig = plot_consumer_dashboard(history, show=False)
    if fig:
        path = f"{output_dir}/consumer_dashboard.png"
        fig.savefig(path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        saved['consumer_dashboard'] = path
        print(f"  - Consumer dashboard saved")

    # Policymaker Dashboard
    fig = plot_policymaker_dashboard(history, show=False)
    if fig:
        path = f"{output_dir}/policymaker_dashboard.png"
        fig.savefig(path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        saved['policymaker_dashboard'] = path
        print(f"  - Policymaker dashboard saved")

    # Evaluator Dashboard
    fig = plot_evaluator_dashboard(history, show=False)
    if fig:
        path = f"{output_dir}/evaluator_dashboard.png"
        fig.savefig(path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        saved['evaluator_dashboard'] = path
        print(f"  - Evaluator dashboard saved")

    # Summary Dashboard
    fig = plot_summary_dashboard(history, show=False)
    if fig:
        path = f"{output_dir}/summary_dashboard.png"
        fig.savefig(path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        saved['summary_dashboard'] = path
        print(f"  - Summary dashboard saved")

    # Investment Comparison
    fig = plot_investment_comparison(history, show=False)
    if fig:
        path = f"{output_dir}/investment_comparison.png"
        fig.savefig(path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        saved['investment_comparison'] = path
        print(f"  - Investment comparison saved")

    # Validity Over Time
    if len(history) >= 5:
        fig = plot_validity_over_time(history, show=False)
        if fig:
            path = f"{output_dir}/validity_over_time.png"
            fig.savefig(path, dpi=150, bbox_inches='tight')
            plt.close(fig)
            saved['validity_over_time'] = path
            print(f"  - Validity over time saved")

    print(f"\nAll dashboards saved to: {output_dir}")
    return saved


# =============================================================================
# Legacy Compatibility (maps old function names to new ones)
# =============================================================================

def plot_simulation_results(history, save_path=None, show=True):
    """Legacy function - redirects to plot_provider_dashboard."""
    return plot_provider_dashboard(history, save_path, show)


def plot_strategy_evolution(history, save_path=None, show=True):
    """Legacy function - redirects to plot_investment_comparison."""
    return plot_investment_comparison(history, save_path, show)


def plot_belief_accuracy(history, save_path=None, show=True):
    """Plot belief accuracy (kept for compatibility)."""
    if not history:
        return None

    providers = get_providers(history)
    provider_colors = {p: c for p, c in zip(providers, get_provider_colors(len(providers)))}
    rounds = [h["round"] for h in history]

    fig, ax = plt.subplots(figsize=(10, 5))

    for provider in providers:
        true_caps = np.array([h["true_capabilities"][provider] for h in history])
        believed_caps = np.array([h["believed_capabilities"][provider] for h in history])
        belief_error = believed_caps - true_caps
        ax.plot(rounds, belief_error, 'o-', label=provider, color=provider_colors[provider],
                markersize=4, linewidth=2)

    ax.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    ax.fill_between(rounds, -0.05, 0.05, alpha=0.1, color='green', label='Accurate zone')

    style_axis(ax, "Belief Accuracy (Believed - True Capability)", "Round", "Error")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


def plot_consumer_satisfaction(history, save_path=None, show=True):
    """Legacy function - redirects to plot_consumer_dashboard."""
    return plot_consumer_dashboard(history, save_path, show)


def plot_policymaker_interventions(history, save_path=None, show=True):
    """Legacy function - redirects to plot_policymaker_dashboard."""
    return plot_policymaker_dashboard(history, save_path, show)


def plot_ecosystem_dashboard(history, save_path=None, show=True):
    """Legacy function - redirects to plot_summary_dashboard."""
    return plot_summary_dashboard(history, save_path, show)


def create_all_plots(history, output_dir="./plots", show=True):
    """Legacy function - redirects to create_all_dashboards."""
    return create_all_dashboards(history, output_dir, show)


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    # Test with a simulation
    from simulation import run_default_simulation

    print("Running simulation...")
    sim = run_default_simulation()

    print("\nCreating dashboards...")
    create_all_dashboards(sim.history, output_dir="./test_plots", show=False)
