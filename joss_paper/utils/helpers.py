import numpy as np
import matplotlib.pyplot as plt

def plot_stacked_bar(
    df,
    scenarios,
    title,
    y_label="Value",
    scenario_labels=None,
    ylim=None,
    figsize=(8, 6),
    cmap="tab20",
):
    """
    Plots a stacked bar chart with negative values stacked downward.

    Parameters
    ----------
    df : pandas.DataFrame
        Index: categories. Columns: scenario names (must match 'scenarios').
    scenarios : list
        List of scenario names (must match df columns).
    y_label : str, optional
        Label for the y-axis.
    title : str, optional
        Plot title.
    scenario_labels : list, optional
        Labels for x-ticks. Defaults to scenarios.
    ylim : tuple or None, optional
        y-axis limits (min, max). If None, auto-scaled.
    figsize : tuple, optional
        Size of the figure.
    cmap : str, optional
        Matplotlib colormap name for bars.

    Returns
    -------
    fig, ax : matplotlib Figure and Axes
    """
    categories = df.index.tolist()
    bar_x = np.arange(len(scenarios))
    colors = plt.get_cmap(cmap).colors
    cat_colors = {cat: colors[i % len(colors)] for i, cat in enumerate(categories)}

    fig, ax = plt.subplots(figsize=figsize)
    bottom_pos = np.zeros(len(scenarios))
    bottom_neg = np.zeros(len(scenarios))
    legend_added = set()

    for cat in categories:
        values = df.loc[cat, scenarios].values
        bar_pos = np.where(values > 0, values, 0)
        bar_neg = np.where(values < 0, values, 0)
        label = cat if cat not in legend_added else None

        # Plot positive stack
        ax.bar(
            bar_x, bar_pos, width=0.6, bottom=bottom_pos,
            label=label, color=cat_colors[cat]
        )
        bottom_pos += bar_pos
        # Plot negative stack
        ax.bar(
            bar_x, bar_neg, width=0.6, bottom=bottom_neg,
            color=cat_colors[cat]
        )
        bottom_neg += bar_neg
        if label:
            legend_added.add(cat)

    ax.set_xticks(bar_x)
    ax.set_xticklabels(scenario_labels if scenario_labels else scenarios)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.axhline(0, color='black', linewidth=0.8)
    if ylim:
        ax.set_ylim(*ylim)
    ax.legend(title="Category", bbox_to_anchor=(1.05, 1), loc='upper left')
    fig.tight_layout()
    return fig, ax