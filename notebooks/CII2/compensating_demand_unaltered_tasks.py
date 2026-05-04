from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.patches import FancyBboxPatch, Patch


BG_COLOR = "#fafafa"
TEXT_COLOR = "#000000"
GRID_COLOR = "#cfcfcf"
LOW_COLOR = "#000000"
HIGH_COLOR = "#000000"
BOOKKEEPER_COLOR = "#8AAE92"
BOOKKEEPER_FILL = "#EEF5F0"
ANALYST_COLOR = "#C45D2D"
ANALYST_FILL = "#FCEEE9"


def outlined_text(ax, x, y, text, size=12, color=TEXT_COLOR, ha="center", va="center", weight=None):
    label = ax.text(
        x,
        y,
        text,
        fontsize=size,
        color=color,
        ha=ha,
        va=va,
        fontweight=weight,
        zorder=5,
    )
    label.set_path_effects([path_effects.withStroke(linewidth=4, foreground=BG_COLOR)])
    return label


def add_task_box(ax, x, y, text, color, fill_color, width=2.35, height=0.92):
    box = FancyBboxPatch(
        (x - width / 2, y - height / 2),
        width,
        height,
        boxstyle="round,pad=0.08,rounding_size=0.05",
        linewidth=1.5,
        edgecolor=color,
        facecolor=fill_color,
        zorder=3,
    )
    ax.add_patch(box)
    outlined_text(ax, x, y, text, size=13, color=TEXT_COLOR)


def main():
    output_dir = Path(__file__).resolve().parent / "outputs"
    output_dir.mkdir(exist_ok=True)

    fig, ax = plt.subplots(figsize=(12.5, 5.8))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(-0.2, 10.2)
    ax.set_ylim(-1.08, 3.35)
    ax.axis("off")

    fig.suptitle(
        "Compensating Demand for Unaltered Tasks",
        fontsize=23,
        fontweight="bold",
        y=0.965,
        color="black",
    )

    y_axis = 1.15
    ax.annotate(
        "",
        xy=(10, y_axis),
        xytext=(0, y_axis),
        arrowprops=dict(arrowstyle="-|>", color=TEXT_COLOR, linewidth=2.4, shrinkA=0, shrinkB=0),
        zorder=1,
    )

    tick_positions = [0, 1.45, 4.05, 7.0, 8.95, 10]
    for tick in tick_positions:
        ax.plot([tick, tick], [y_axis - 0.12, y_axis + 0.12], color=TEXT_COLOR, linewidth=1.4, zorder=2)

    outlined_text(ax, 0, y_axis - 0.45, "Low", size=13, color=LOW_COLOR, weight="bold")
    outlined_text(ax, 10, y_axis - 0.45, "High", size=13, color=HIGH_COLOR, weight="bold")
    outlined_text(ax, 5, y_axis - 0.65, "Compensating demand", size=16, color=TEXT_COLOR, weight="bold")

    box_specs = [
        (1.45, 2.55, "Handle physical\ncash deposits", 2.35, BOOKKEEPER_COLOR, BOOKKEEPER_FILL),
        (4.05, -0.52, "Field vendor\ninquiries", 2.35, BOOKKEEPER_COLOR, BOOKKEEPER_FILL),
        (7.0, 2.55, "Client relationship\nmanagement", 2.55, ANALYST_COLOR, ANALYST_FILL),
        (8.85, -0.52, "Portfolio risk analysis", 2.55, ANALYST_COLOR, ANALYST_FILL),
    ]

    for x, y, *_ in box_specs:
        if y > y_axis:
            ax.plot(
                [x, x],
                [y_axis + 0.12, y - 0.54],
                color=GRID_COLOR,
                linewidth=1.1,
                linestyle="--",
                zorder=1,
            )
        else:
            ax.plot(
                [x, x],
                [y_axis - 0.12, y + 0.54],
                color=GRID_COLOR,
                linewidth=1.1,
                linestyle="--",
                zorder=1,
            )

    for x, y, text, width, color, fill_color in box_specs:
        add_task_box(ax, x, y, text, color, fill_color, width=width)

    legend_handles = [
        Patch(facecolor=BOOKKEEPER_FILL, edgecolor=BOOKKEEPER_COLOR, linewidth=1.5, label="Bookkeeper tasks"),
        Patch(facecolor=ANALYST_FILL, edgecolor=ANALYST_COLOR, linewidth=1.5, label="Financial analyst tasks"),
    ]
    fig.legend(
        handles=legend_handles,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.025),
        ncol=2,
        frameon=True,
        framealpha=1,
        facecolor="white",
        edgecolor="#dddddd",
        fontsize=11,
    )

    plt.subplots_adjust(top=0.86, bottom=0.15, left=0.035, right=0.965)
    output_path = "compensating_demand_unaltered_tasks.png"
    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()
