"""
Plotting utilities for Evaluation Ecosystem Simulation

Provides dashboards for each actor type and a summary dashboard.
Scalable to N providers/actors.
"""
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
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
    """Compute rolling correlation between scores and true capabilities.

    Returns (rounds, correlations) where rounds are actual round numbers
    (from history[i]["round"]), not array indices.
    """
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
                # Use actual round number from history, not array index
                rounds_used.append(history[i - 1]["round"])

    return rounds_used, correlations


def compute_per_benchmark_rolling_correlation(history: list, window_size: int = 5) -> dict:
    """Compute rolling correlation per benchmark.

    Returns {benchmark_name: (rounds, correlations)} where each benchmark
    gets its own validity correlation over time.
    """
    if len(history) < window_size:
        return {}

    # Check if we have per-benchmark data
    if not history or "per_benchmark_scores" not in history[0]:
        return {}

    providers = get_providers(history)

    # Get all benchmark names across all rounds
    all_benchmarks = set()
    for h in history:
        if "per_benchmark_scores" in h:
            all_benchmarks.update(h["per_benchmark_scores"].keys())

    benchmark_correlations = {}

    for benchmark in all_benchmarks:
        correlations = []
        rounds_used = []

        for i in range(window_size, len(history) + 1):
            window = history[i - window_size:i]
            benchmark_scores = []
            benchmark_caps = []

            for h in window:
                per_bm = h.get("per_benchmark_scores", {})
                if benchmark in per_bm:
                    for provider in providers:
                        if provider in per_bm[benchmark]:
                            benchmark_scores.append(per_bm[benchmark][provider])
                            benchmark_caps.append(h["true_capabilities"][provider])

            if len(benchmark_scores) >= 2:
                corr = np.corrcoef(benchmark_scores, benchmark_caps)[0, 1]
                if not np.isnan(corr):
                    correlations.append(corr)
                    rounds_used.append(history[i - 1]["round"])

        if correlations:
            benchmark_correlations[benchmark] = (rounds_used, correlations)

    return benchmark_correlations


def categorize_headline(headline: str) -> str:
    """Classify a media headline into one of 7 categories via substring matching."""
    hl = headline.lower()
    if "takes the lead" in hl or "takes #1" in hl:
        return "leader_change"
    if "surges by" in hl:
        return "score_surge"
    if any(kw in hl for kw in ("investigation", "warning", "mandate", "audit")):
        return "regulatory"
    if "raises $" in hl:
        return "funding"
    if "surge in adoption" in hl or "turning away" in hl:
        return "consumer"
    if "benchmark" in hl or "validity" in hl:
        return "benchmark"
    return "other"


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
        ax2.plot(rounds, true_caps, '-', color=provider_colors[provider], linewidth=2)
        ax2.plot(rounds, believed_caps, '--', color=provider_colors[provider],
                 linewidth=1.5, alpha=0.6)
    # Legend: provider colors + line-style key
    handles = [
        mlines.Line2D([], [], color=provider_colors[p], linewidth=2, label=p)
        for p in providers
    ]
    handles.append(mlines.Line2D([], [], color='gray', linestyle='-', linewidth=2, label='True'))
    handles.append(mlines.Line2D([], [], color='gray', linestyle='--', linewidth=1.5,
                                  alpha=0.6, label='Believed'))
    ax2.legend(handles=handles, loc='best', fontsize=7)
    style_axis(ax2, "True vs Believed Capability", "Round", "Capability", legend=False)

    # --- Panel 3: Investment Portfolio (all providers in grid) ---
    ax3 = axes[0, 2]
    ax3.axis('off')  # Turn off main axis, we'll use subplots

    investment_types = ["fundamental_research", "training_optimization",
                        "evaluation_engineering", "safety_alignment"]

    # Create grid of subplots within Panel 3
    from matplotlib.gridspec import GridSpecFromSubplotSpec

    # Determine grid layout based on number of providers
    if n_providers <= 2:
        grid_rows, grid_cols = 1, 2
    elif n_providers <= 4:
        grid_rows, grid_cols = 2, 2
    elif n_providers <= 6:
        grid_rows, grid_cols = 2, 3
    else:
        grid_rows, grid_cols = 3, 3

    gs = GridSpecFromSubplotSpec(grid_rows, grid_cols, subplot_spec=ax3.get_subplotspec(),
                                  hspace=0.4, wspace=0.3)

    for idx, provider in enumerate(providers):
        if idx >= grid_rows * grid_cols:
            break

        row = idx // grid_cols
        col = idx % grid_cols
        sub_ax = fig.add_subplot(gs[row, col])

        # Stacked area chart for this provider
        bottom = np.zeros(len(rounds))
        for inv_type in investment_types:
            values = np.array(extract_investment(history, provider, inv_type))
            sub_ax.fill_between(rounds, bottom, bottom + values,
                               alpha=0.7, color=inv_colors[inv_type])
            bottom += values

        sub_ax.set_ylim(0, 1.05)
        sub_ax.set_title(provider, fontsize=8, fontweight='bold')
        sub_ax.tick_params(labelsize=6)
        sub_ax.grid(True, alpha=0.2)

        # Only show x-label on bottom row
        if row == grid_rows - 1:
            sub_ax.set_xlabel("Round", fontsize=7)
        # Only show y-label on left column
        if col == 0:
            sub_ax.set_ylabel("Allocation", fontsize=7)

    # Add single legend for all subplots (outside the grid)
    legend_elements = [
        mpatches.Patch(facecolor=inv_colors[inv_type], alpha=0.7,
                      label=inv_type.replace("_", " ").title()[:12])
        for inv_type in investment_types
    ]
    ax3.legend(handles=legend_elements, loc='upper center',
              bbox_to_anchor=(0.5, 1.15), ncol=2, fontsize=7, frameon=False)

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
    figsize: tuple = (20, 10),
) -> Optional[plt.Figure]:
    """
    Create a dashboard for Consumer actors.

    Panels:
    1. Satisfaction by Use Case (profession)
    2. Switching Rate by Use Case (stacked bar)
    3. Switching Rate by Archetype (stacked bar)
    4. Market Share (subscriptions per provider)
    5. Per-Provider Satisfaction
    6. Satisfaction Gap (Score - Satisfaction)

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

    fig, axes = plt.subplots(2, 3, figsize=figsize)
    fig.suptitle("Consumer Dashboard", fontsize=14, fontweight='bold')

    # --- Panel 1: Satisfaction by Use Case ---
    ax1 = axes[0, 0]

    # Extract use cases and compute average satisfaction per use case
    use_cases_set = set()
    for h in consumer_rounds:
        segment_data = h["consumer_data"].get("segment_data", {})
        for seg_name, seg_info in segment_data.items():
            use_case = seg_info.get("use_case")
            if use_case:
                use_cases_set.add(use_case)

    use_cases = sorted(use_cases_set)
    use_case_colors = get_provider_colors(len(use_cases))

    for i, use_case in enumerate(use_cases):
        use_case_satisfaction = []
        for h in consumer_rounds:
            segment_data = h["consumer_data"].get("segment_data", {})
            # Aggregate satisfaction across all segments with this use_case
            total_sat = 0.0
            count = 0
            for seg_name, seg_info in segment_data.items():
                if seg_info.get("use_case") == use_case:
                    # Average satisfaction across all providers in this segment
                    seg_sats = seg_info.get("satisfaction", {}).values()
                    if seg_sats:
                        total_sat += sum(seg_sats) / len(seg_sats)
                        count += 1
            if count > 0:
                use_case_satisfaction.append(total_sat / count)
            else:
                use_case_satisfaction.append(0)

        ax1.plot(rounds, use_case_satisfaction, 'o-', label=use_case,
                color=use_case_colors[i], markersize=3, linewidth=1.5)

    ax1.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
    ax1.set_ylim(0, 1)
    style_axis(ax1, "Satisfaction by Use Case", "Round", "Satisfaction")

    # --- Panel 2: Switching Rate by Use Case (stacked bar) ---
    ax2 = axes[0, 1]

    # Aggregate switching by use_case across archetypes
    use_case_switching = {uc: [] for uc in use_cases}
    for h in consumer_rounds:
        segment_data = h["consumer_data"].get("segment_data", {})
        use_case_totals = {uc: 0.0 for uc in use_cases}

        for seg_name, seg_info in segment_data.items():
            use_case = seg_info.get("use_case")
            if use_case in use_cases:
                # Switching rate × market_fraction = contribution to total switching
                seg_switching = seg_info.get("switching_rate", 0.0)
                market_frac = seg_info.get("market_fraction", 0.0)
                use_case_totals[use_case] += seg_switching * market_frac

        for uc in use_cases:
            use_case_switching[uc].append(use_case_totals[uc] * 100)  # Convert to %

    # Stacked bar chart
    bottom = np.zeros(len(rounds))
    for i, use_case in enumerate(use_cases):
        values = np.array(use_case_switching[use_case])
        ax2.bar(rounds, values, bottom=bottom, label=use_case,
                color=use_case_colors[i], alpha=0.8, width=0.8)
        bottom += values

    ax2.set_ylabel("Switching Rate (%)", fontsize=9)
    ax2.legend(loc='upper right', fontsize=6)
    style_axis(ax2, "Switching Rate by Use Case", "Round", "Switching Rate (%)", legend=False)

    # --- Panel 3: Switching Rate by Archetype (stacked bar) ---
    ax3 = axes[0, 2]

    # Extract archetypes and aggregate switching
    archetypes_set = set()
    for h in consumer_rounds:
        segment_data = h["consumer_data"].get("segment_data", {})
        for seg_name, seg_info in segment_data.items():
            archetype = seg_info.get("archetype")
            if archetype:
                archetypes_set.add(archetype)

    archetypes = sorted(archetypes_set)
    archetype_colors = get_provider_colors(len(archetypes))

    archetype_switching = {arch: [] for arch in archetypes}
    for h in consumer_rounds:
        segment_data = h["consumer_data"].get("segment_data", {})
        archetype_totals = {arch: 0.0 for arch in archetypes}

        for seg_name, seg_info in segment_data.items():
            archetype = seg_info.get("archetype")
            if archetype in archetypes:
                seg_switching = seg_info.get("switching_rate", 0.0)
                market_frac = seg_info.get("market_fraction", 0.0)
                archetype_totals[archetype] += seg_switching * market_frac

        for arch in archetypes:
            archetype_switching[arch].append(archetype_totals[arch] * 100)

    # Stacked bar chart
    bottom = np.zeros(len(rounds))
    for i, archetype in enumerate(archetypes):
        values = np.array(archetype_switching[archetype])
        ax3.bar(rounds, values, bottom=bottom, label=archetype.replace("_", " ").title(),
                color=archetype_colors[i], alpha=0.8, width=0.8)
        bottom += values

    ax3.set_ylabel("Switching Rate (%)", fontsize=9)
    ax3.legend(loc='upper right', fontsize=7)
    style_axis(ax3, "Switching Rate by Archetype", "Round", "Switching Rate (%)", legend=False)

    # --- Panel 4: Market Share Over Time ---
    ax4 = axes[1, 0]

    # Use market_shares (proportions) from consumer_data
    market_share = {p: [] for p in providers}
    for h in consumer_rounds:
        shares = h["consumer_data"].get("market_shares", {})
        for p in providers:
            market_share[p].append(shares.get(p, 0))

    # Stacked area chart
    bottom = np.zeros(len(rounds))
    for provider in providers:
        values = np.array(market_share[provider])
        ax4.fill_between(rounds, bottom, bottom + values,
                        alpha=0.7, label=provider, color=provider_colors[provider])
        bottom += values

    ax4.set_ylim(0, 1.05)
    style_axis(ax4, "Market Share", "Round", "Share")

    # --- Panel 5: Per-Provider Satisfaction ---
    ax5 = axes[1, 1]

    avg_satisfaction = [h["consumer_data"].get("avg_satisfaction", 0) for h in consumer_rounds]

    for provider in providers:
        prov_sats = []
        for h in consumer_rounds:
            prov_sat = h["consumer_data"].get("provider_satisfaction", {})
            prov_sats.append(prov_sat.get(provider, 0))
        ax5.plot(rounds, prov_sats, 'o-', label=provider, color=provider_colors[provider],
                 markersize=3, linewidth=2)

    ax5.plot(rounds, avg_satisfaction, 'k--', linewidth=1.5, alpha=0.5, label='Market Avg')
    ax5.set_ylim(0, 1)
    style_axis(ax5, "Per-Provider Satisfaction", "Round", "Satisfaction")

    # --- Panel 6: Satisfaction Gap (Score - Satisfaction) ---
    ax6 = axes[1, 2]

    for provider in providers:
        scores = [h["scores"][provider] for h in consumer_rounds]
        prov_sats = [h["consumer_data"].get("provider_satisfaction", {}).get(provider, 0)
                     for h in consumer_rounds]
        gap = [s - sat for s, sat in zip(scores, prov_sats)]
        ax6.plot(rounds, gap, 'o-', label=provider, color=provider_colors[provider],
                 markersize=3, linewidth=2)
    ax6.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    style_axis(ax6, "Satisfaction Gap (Score - Satisfaction)", "Round", "Gap")

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
        # Collect ALL benchmark names across all rounds (handles mid-simulation introductions)
        all_benchmark_names = set()
        for h in history:
            if "benchmark_params" in h:
                all_benchmark_names.update(h["benchmark_params"].keys())

        # Sort benchmarks by first appearance (maintains introduction order)
        benchmark_first_appearance = {}
        for h in history:
            if "benchmark_params" in h:
                for bm in h["benchmark_params"].keys():
                    if bm not in benchmark_first_appearance:
                        benchmark_first_appearance[bm] = h["round"]

        benchmark_names = sorted(all_benchmark_names,
                                 key=lambda bm: benchmark_first_appearance.get(bm, 0))
        bench_colors = get_provider_colors(len(benchmark_names))

        # Plot average score per benchmark over time
        for i, bench_name in enumerate(benchmark_names):
            bench_avgs = []
            bench_rounds = []  # Track rounds where this benchmark exists
            for h in history:
                bench_scores = h.get("per_benchmark_scores", {}).get(bench_name, {})
                if bench_scores:
                    bench_avgs.append(np.mean(list(bench_scores.values())))
                    bench_rounds.append(h["round"])

            # Only plot if benchmark has data
            if bench_avgs:
                ax3.plot(bench_rounds, bench_avgs, 'o-', label=bench_name,
                        color=bench_colors[i], markersize=3, linewidth=2)

                # Mark introduction round if not round 0
                intro_round = benchmark_first_appearance[bench_name]
                if intro_round > 0:
                    ax3.axvline(x=intro_round, color=bench_colors[i],
                               linestyle=':', alpha=0.3, linewidth=1)

        ax3.set_ylim(0, 1.05)
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
    metadata: Optional[dict] = None,
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
        metadata: Optional dict with experiment metadata (n_rounds, llm_mode,
                  n_consumers, n_policymakers, etc.)

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

    # Build title with metadata
    title = "Evaluation Ecosystem Summary Dashboard"
    subtitle_parts = []

    # Extract info from history
    n_rounds = len(history)
    provider_names = ", ".join(providers)
    subtitle_parts.append(f"{n_rounds} rounds")
    subtitle_parts.append(f"Providers: {provider_names}")

    has_funders = any("funder_data" in h for h in history)

    # Add metadata if provided
    if metadata:
        if metadata.get("llm_mode"):
            subtitle_parts.append("LLM mode")
        else:
            subtitle_parts.append("Heuristic mode")
        if "n_consumers" in metadata and metadata["n_consumers"] > 0:
            subtitle_parts.append(f"{metadata['n_consumers']} consumers")
        if "n_policymakers" in metadata and metadata["n_policymakers"] > 0:
            subtitle_parts.append(f"{metadata['n_policymakers']} policymaker(s)")
        if "n_funders" in metadata and metadata["n_funders"] > 0:
            subtitle_parts.append(f"{metadata['n_funders']} funder(s)")
    else:
        # Infer from history
        if has_consumers:
            # Check for segment-based consumer market
            for h in history:
                if "consumer_data" in h:
                    cd = h["consumer_data"]
                    if "segment_data" in cd:
                        n_segments = len(cd["segment_data"])
                        subtitle_parts.append(f"{n_segments} market segments")
                    elif "subscriptions" in cd:
                        n_consumers = len(cd["subscriptions"])
                        subtitle_parts.append(f"{n_consumers} consumers")
                    break
        if has_policymakers:
            subtitle_parts.append("1 policymaker")
        if has_funders:
            subtitle_parts.append("funders enabled")

    subtitle = " | ".join(subtitle_parts)
    fig.suptitle(f"{title}\n{subtitle}", fontsize=14, fontweight='bold')

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
    # Legend: one entry per provider (colored) + line-style entries
    handles = [
        mlines.Line2D([], [], color=provider_colors[p], linewidth=2, label=p)
        for p in providers
    ]
    handles.append(mlines.Line2D([], [], color='gray', linestyle='-', linewidth=2, label='True'))
    handles.append(mlines.Line2D([], [], color='gray', linestyle='--', linewidth=1.5,
                                  alpha=0.6, label='Believed'))
    ax.legend(handles=handles, loc='best', fontsize=7)
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

    # Try per-benchmark correlations
    per_benchmark = compute_per_benchmark_rolling_correlation(history)

    if per_benchmark:
        # Plot per-benchmark correlations
        benchmark_names = sorted(per_benchmark.keys())
        bm_colors = get_provider_colors(len(benchmark_names))

        for i, benchmark in enumerate(benchmark_names):
            bm_rounds, bm_corrs = per_benchmark[benchmark]
            ax.plot(bm_rounds, bm_corrs, 'o-', label=benchmark,
                   color=bm_colors[i], markersize=3, linewidth=1.5)

        # Overall as dashed line
        validity_rounds, validity_values = compute_rolling_correlation(history)
        if validity_values:
            ax.plot(validity_rounds, validity_values, '--', color='black',
                   linewidth=2, alpha=0.5, label='Overall')

        ax.legend(loc='best', fontsize=7)
    else:
        # Fallback to overall
        validity_rounds, validity_values = compute_rolling_correlation(history)
        if validity_values:
            ax.plot(validity_rounds, validity_values, 'o-', color='#2A9D8F',
                    markersize=4, linewidth=2)

    ax.axhline(y=0.7, color='green', linestyle=':', alpha=0.3)
    ax.axhline(y=0.5, color='orange', linestyle=':', alpha=0.3)
    ax.axhline(y=0.3, color='red', linestyle=':', alpha=0.3)
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
                shares = h["consumer_data"].get("market_shares", {})
                for p in providers:
                    market_share[p].append(shares.get(p, 0))

            bottom = np.zeros(len(plot_rounds))
            for provider in providers:
                values = np.array(market_share[provider])
                ax.fill_between(plot_rounds, bottom, bottom + values, alpha=0.7,
                               label=provider, color=provider_colors[provider])
                bottom += values
            ax.set_ylim(0, 1.05)
    style_axis(ax, "Market Share", "Round", "Share")
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
    """Plot rolling validity correlation, broken down by benchmark if available."""
    if len(history) < window_size:
        print(f"Need at least {window_size} rounds")
        return None

    # Try per-benchmark correlations first
    per_benchmark = compute_per_benchmark_rolling_correlation(history, window_size)

    fig, ax = plt.subplots(figsize=(12, 6))

    if per_benchmark:
        # Plot per-benchmark correlations
        benchmark_names = sorted(per_benchmark.keys())
        colors = get_provider_colors(len(benchmark_names))

        for i, benchmark in enumerate(benchmark_names):
            rounds, correlations = per_benchmark[benchmark]
            ax.plot(rounds, correlations, 'o-', label=benchmark,
                   color=colors[i], markersize=4, linewidth=2)

        # Also plot overall correlation as a thicker dashed line
        validity_rounds, validity_values = compute_rolling_correlation(history, window_size)
        if validity_values:
            ax.plot(validity_rounds, validity_values, '--', color='black',
                   linewidth=2.5, alpha=0.6, label='Overall')

        title = f"Benchmark Validity by Benchmark (window={window_size})"
    else:
        # Fallback to overall correlation
        validity_rounds, validity_values = compute_rolling_correlation(history, window_size)
        if not validity_values:
            return None

        ax.plot(validity_rounds, validity_values, 'o-', color='#2A9D8F',
                markersize=5, linewidth=2, label='Overall')
        title = f"Benchmark Validity Over Time (window={window_size})"

    ax.axhline(y=0.7, color='green', linestyle=':', alpha=0.4, linewidth=1)
    ax.axhline(y=0.5, color='orange', linestyle=':', alpha=0.4, linewidth=1)
    ax.axhline(y=0.3, color='red', linestyle=':', alpha=0.4, linewidth=1)
    ax.set_ylim(-0.2, 1.0)

    style_axis(ax, title, "Round", "Correlation (Score vs True Capability)")

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
# Funder Dashboard
# =============================================================================

def plot_funder_dashboard(
    history: list,
    save_path: Optional[str] = None,
    show: bool = True,
    figsize: tuple = (20, 10),
) -> Optional[plt.Figure]:
    """
    Create a dashboard for Funder actors.

    Panels:
    1. Funding Allocations Over Time (stacked area)
    2. Provider Funding Multipliers Over Time
    3. Total Funding Deployed
    4. Funder ROI Tracking (inferred from provider performance)

    Args:
        history: List of round data dicts
        save_path: Path to save figure
        show: Whether to display
        figsize: Figure size

    Returns:
        matplotlib Figure or None
    """
    funder_rounds = [h for h in history if "funder_data" in h]
    if not funder_rounds:
        print("No funder data to plot")
        return None

    providers = get_providers(history)
    provider_colors = {p: c for p, c in zip(providers, get_provider_colors(len(providers)))}

    rounds = [h["round"] for h in funder_rounds]

    fig, axes = plt.subplots(2, 3, figsize=figsize)
    fig.suptitle("Funder Dashboard", fontsize=14, fontweight='bold')

    # --- Panel 1: Funding Allocations Over Time (stacked area) ---
    ax1 = axes[0, 0]

    # Aggregate funding per provider across all funders
    funding_per_provider = {p: [] for p in providers}
    for h in funder_rounds:
        fd = h["funder_data"]
        allocations = fd.get("allocations", {})
        # Sum across all funders
        provider_totals = {p: 0 for p in providers}
        for funder_allocs in allocations.values():
            if isinstance(funder_allocs, dict):
                for provider, amount in funder_allocs.items():
                    if provider in provider_totals:
                        provider_totals[provider] += amount
        for p in providers:
            funding_per_provider[p].append(provider_totals.get(p, 0))

    # Stacked area chart
    bottom = np.zeros(len(rounds))
    for provider in providers:
        values = np.array(funding_per_provider[provider])
        # Convert to thousands for readability
        values_k = values / 1000
        ax1.fill_between(rounds, bottom, bottom + values_k, alpha=0.7,
                        label=provider, color=provider_colors[provider])
        bottom += values_k

    ax1.set_xlabel("Round", fontsize=9)
    ax1.set_ylabel("Funding ($K)", fontsize=9)
    ax1.legend(loc='upper right', fontsize=8)
    ax1.grid(True, alpha=0.3)
    ax1.set_title("Funding Allocations Over Time", fontsize=11, fontweight='bold')

    # --- Panel 2: Provider Funding Multipliers Over Time ---
    ax2 = axes[0, 1]

    for provider in providers:
        multipliers = []
        for h in funder_rounds:
            fd = h["funder_data"]
            mult = fd.get("funding_multipliers", {}).get(provider, 1.0)
            multipliers.append(mult)
        ax2.plot(rounds, multipliers, 'o-', label=provider, color=provider_colors[provider],
                 markersize=4, linewidth=2)

    ax2.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, label='No Funding')
    ax2.set_ylim(0.9, 2.1)
    style_axis(ax2, "Funding Multipliers Over Time", "Round", "Multiplier")

    # --- Panel 3: Total Funding Deployed ---
    ax3 = axes[1, 0]

    total_funding = [h["funder_data"].get("total_funding", 0) / 1000 for h in funder_rounds]
    ax3.fill_between(rounds, 0, total_funding, alpha=0.5, color='#2A9D8F')
    ax3.plot(rounds, total_funding, 'o-', color='#2A9D8F', markersize=4, linewidth=2)
    ax3.set_xlabel("Round", fontsize=9)
    ax3.set_ylabel("Total Funding ($K)", fontsize=9)
    ax3.grid(True, alpha=0.3)
    ax3.set_title("Total Funding Deployed", fontsize=11, fontweight='bold')

    # --- Panel 4: Provider Performance vs Funding (scatter) ---
    ax4 = axes[1, 1]

    # For each provider, plot funding received vs capability growth
    # Use data from all rounds
    for provider in providers:
        # Get average funding multiplier
        avg_multiplier = np.mean([
            h["funder_data"].get("funding_multipliers", {}).get(provider, 1.0)
            for h in funder_rounds
        ])

        # Get capability growth
        if len(history) >= 2:
            initial_cap = history[0]["true_capabilities"].get(provider, 0.5)
            final_cap = history[-1]["true_capabilities"].get(provider, 0.5)
            cap_growth = final_cap - initial_cap
        else:
            cap_growth = 0

        ax4.scatter(avg_multiplier, cap_growth, s=150, color=provider_colors[provider],
                   label=provider, alpha=0.8, edgecolors='black', linewidth=1)

    ax4.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax4.axvline(x=1.0, color='gray', linestyle='--', alpha=0.5)
    ax4.set_xlabel("Average Funding Multiplier", fontsize=9)
    ax4.set_ylabel("Capability Growth", fontsize=9)
    ax4.legend(loc='best', fontsize=8)
    ax4.grid(True, alpha=0.3)
    ax4.set_title("Funding Impact on Capability Growth", fontsize=11, fontweight='bold')

    # --- Panel 5: Per-Funder Top Allocation ---
    ax5 = axes[0, 2]
    funder_names = set()
    for h in funder_rounds:
        funder_names.update(h["funder_data"].get("allocations", {}).keys())
    funder_names = sorted(funder_names)

    funder_line_colors = get_provider_colors(len(funder_names))
    for i, funder in enumerate(funder_names):
        top_allocs = []
        for h in funder_rounds:
            allocs = h["funder_data"].get("allocations", {}).get(funder, {})
            if isinstance(allocs, dict) and allocs:
                top_allocs.append(max(allocs.values()) / 1_000_000)
            else:
                top_allocs.append(0)
        ax5.plot(rounds, top_allocs, 'o-', label=funder, color=funder_line_colors[i],
                 markersize=3, linewidth=2)
    ax5.set_xlabel("Round", fontsize=9)
    ax5.set_ylabel("Top Allocation ($M)", fontsize=9)
    ax5.legend(loc='best', fontsize=7)
    ax5.grid(True, alpha=0.3)
    ax5.set_title("Per-Funder Top Allocation", fontsize=11, fontweight='bold')

    # --- Panel 6: Score Momentum (3-Round Avg Delta) ---
    ax6 = axes[1, 2]
    for provider in providers:
        scores = [h["scores"][provider] for h in history]
        # Compute rolling 3-round average of score deltas
        deltas = [scores[i] - scores[i - 1] for i in range(1, len(scores))]
        window = 3
        if len(deltas) >= window:
            momentum = []
            momentum_rounds = []
            for i in range(window - 1, len(deltas)):
                avg_delta = np.mean(deltas[i - window + 1:i + 1])
                momentum.append(avg_delta)
                # Round index corresponds to the end of the window
                momentum_rounds.append(history[i + 1]["round"])
            ax6.plot(momentum_rounds, momentum, 'o-', label=provider,
                     color=provider_colors[provider], markersize=3, linewidth=2)
    ax6.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    style_axis(ax6, "Score Momentum (3-Round Avg Delta)", "Round", "Avg Delta")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Funder dashboard saved to: {save_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


# =============================================================================
# Media Dashboard
# =============================================================================

def plot_media_dashboard(
    history: list,
    save_path: Optional[str] = None,
    show: bool = True,
    figsize: tuple = (14, 10),
) -> Optional[plt.Figure]:
    """
    Create a dashboard for Media coverage.

    Panels:
    1. Media Sentiment Over Time (line + fill)
    2. Headlines by Category (stacked bar)
    3. Provider Attention Heatmap
    4. Risk Signals Per Round

    Args:
        history: List of round data dicts
        save_path: Path to save figure
        show: Whether to display
        figsize: Figure size

    Returns:
        matplotlib Figure or None
    """
    media_rounds = [h for h in history if "media_data" in h]
    if not media_rounds:
        print("No media data to plot")
        return None

    providers = get_providers(history)
    rounds = [h["round"] for h in media_rounds]

    fig, axes = plt.subplots(2, 2, figsize=figsize)
    fig.suptitle("Media Dashboard", fontsize=14, fontweight='bold')

    # --- Panel 1: Media Sentiment Over Time ---
    ax1 = axes[0, 0]
    sentiments = [h["media_data"].get("sentiment", 0) for h in media_rounds]
    ax1.plot(rounds, sentiments, 'o-', color='#457B9D', markersize=3, linewidth=2)
    sentiments_arr = np.array(sentiments)
    rounds_arr = np.array(rounds)
    ax1.fill_between(rounds_arr, 0, sentiments_arr,
                     where=sentiments_arr >= 0, alpha=0.3, color='green',
                     interpolate=True)
    ax1.fill_between(rounds_arr, 0, sentiments_arr,
                     where=sentiments_arr < 0, alpha=0.3, color='red',
                     interpolate=True)
    ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.5)
    style_axis(ax1, "Media Sentiment Over Time", "Round", "Sentiment", legend=False)

    # --- Panel 2: Headlines by Category (stacked bar) ---
    ax2 = axes[0, 1]
    categories = ["leader_change", "score_surge", "regulatory", "funding",
                  "consumer", "benchmark", "other"]
    cat_colors = {
        "leader_change": "#E63946", "score_surge": "#457B9D",
        "regulatory": "#6A4C93", "funding": "#2A9D8F",
        "consumer": "#F4A261", "benchmark": "#E9C46A", "other": "#CCCCCC",
    }
    # Count categories per round
    cat_counts = {cat: [] for cat in categories}
    for h in media_rounds:
        headlines = h["media_data"].get("headlines", [])
        round_cats = {cat: 0 for cat in categories}
        for headline in headlines:
            cat = categorize_headline(headline)
            round_cats[cat] += 1
        for cat in categories:
            cat_counts[cat].append(round_cats[cat])

    bottom = np.zeros(len(rounds))
    for cat in categories:
        values = np.array(cat_counts[cat])
        ax2.bar(rounds, values, bottom=bottom, label=cat.replace("_", " ").title(),
                color=cat_colors[cat], alpha=0.8, width=0.8)
        bottom += values
    ax2.legend(loc='upper right', fontsize=6)
    ax2.set_xlabel("Round", fontsize=9)
    ax2.set_ylabel("Count", fontsize=9)
    ax2.set_title("Headlines by Category", fontsize=11, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')

    # --- Panel 3: Provider Attention Heatmap ---
    ax3 = axes[1, 0]
    attention_matrix = []
    for p in providers:
        row = []
        for h in media_rounds:
            attn = h["media_data"].get("provider_attention", {})
            row.append(attn.get(p, 0))
        attention_matrix.append(row)
    attention_matrix = np.array(attention_matrix)

    if attention_matrix.size > 0:
        im = ax3.imshow(attention_matrix, aspect='auto', cmap='YlOrRd',
                        vmin=0, vmax=1)
        ax3.set_yticks(range(len(providers)))
        ax3.set_yticklabels(providers, fontsize=8)
        ax3.set_xlabel("Round Index", fontsize=9)
        fig.colorbar(im, ax=ax3, fraction=0.046, pad=0.04)
    ax3.set_title("Provider Attention Heatmap", fontsize=11, fontweight='bold')

    # --- Panel 4: Risk Signals Per Round ---
    ax4 = axes[1, 1]
    risk_counts = [len(h["media_data"].get("risk_signals", [])) for h in media_rounds]
    bar_colors = ['#E63946' if c > 0 else '#CCCCCC' for c in risk_counts]
    ax4.bar(rounds, risk_counts, color=bar_colors, alpha=0.8)
    total_risks = sum(risk_counts)
    ax4.text(0.95, 0.95, f"Total: {total_risks}", transform=ax4.transAxes,
             ha='right', va='top', fontsize=10, fontweight='bold')
    style_axis(ax4, "Risk Signals Per Round", "Round", "Count", legend=False)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Media dashboard saved to: {save_path}")

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
    metadata: Optional[dict] = None,
) -> dict:
    """
    Create and save all dashboards.

    Args:
        history: List of round data dicts
        output_dir: Directory to save plots
        show: Whether to display plots
        metadata: Optional experiment metadata dict with keys like:
                  n_rounds, llm_mode, n_consumers, n_policymakers

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

    # Funder Dashboard
    fig = plot_funder_dashboard(history, show=False)
    if fig:
        path = f"{output_dir}/funder_dashboard.png"
        fig.savefig(path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        saved['funder_dashboard'] = path
        print(f"  - Funder dashboard saved")

    # Media Dashboard
    fig = plot_media_dashboard(history, show=False)
    if fig:
        path = f"{output_dir}/media_dashboard.png"
        fig.savefig(path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        saved['media_dashboard'] = path
        print(f"  - Media dashboard saved")

    # Evaluator Dashboard
    fig = plot_evaluator_dashboard(history, show=False)
    if fig:
        path = f"{output_dir}/evaluator_dashboard.png"
        fig.savefig(path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        saved['evaluator_dashboard'] = path
        print(f"  - Evaluator dashboard saved")

    # Summary Dashboard (with metadata)
    fig = plot_summary_dashboard(history, show=False, metadata=metadata)
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
    # Test with a quick simulation
    from simulation import EvalEcosystemSimulation, SimulationConfig, get_default_provider_configs

    print("Running simulation...")
    config = SimulationConfig(n_rounds=20, seed=42, verbose=True)
    sim = EvalEcosystemSimulation(config)
    sim.setup(get_default_provider_configs())
    sim.run()

    print("\nCreating dashboards...")
    create_all_dashboards(sim.history, output_dir="./test_plots", show=False)
