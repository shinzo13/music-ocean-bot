import io

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

BG = "#16161e"
FG = "#e6e6ef"
MUTED = "#8b8b9e"


def _pie(ax, data: dict[str, int], title: str, palette):
    items = sorted(data.items(), key=lambda kv: -kv[1])
    labels = [k for k, _ in items]
    values = [v for _, v in items]
    total = sum(values)
    wedges, _, autotexts = ax.pie(
        values,
        colors=palette[:len(values)],
        startangle=90,
        counterclock=False,
        autopct=lambda pct: f"{pct:.0f}%" if pct >= 4 else "",
        pctdistance=0.75,
        wedgeprops={"width": 0.45, "edgecolor": BG, "linewidth": 2},
    )
    for t in autotexts:
        t.set_color(FG)
        t.set_fontsize(11)
        t.set_fontweight("bold")
    ax.text(0, 0, f"{total}", ha="center", va="center",
            color=FG, fontsize=22, fontweight="bold")
    ax.set_title(title, color=FG, fontsize=15, fontweight="bold", pad=14)
    ax.legend(
        wedges,
        [f"{l} — {v}" for l, v in items],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.02),
        ncol=2,
        frameon=False,
        labelcolor=FG,
        fontsize=11,
    )


def render_stats_banner(by_engine: dict[str, int], by_context: dict[str, int]) -> bytes:
    sns.set_theme(style="dark")
    fig, axes = plt.subplots(1, 2, figsize=(12, 6.2), facecolor=BG)
    for ax in axes:
        ax.set_facecolor(BG)

    _pie(axes[0], by_context, "by download context", sns.color_palette("muted"))
    _pie(axes[1], by_engine, "by engine", sns.color_palette("deep"))

    fig.suptitle("koshke usage stats", color=MUTED, fontsize=12, y=0.98)
    fig.tight_layout(rect=(0, 0.04, 1, 0.96))

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=160, facecolor=BG, bbox_inches="tight")
    plt.close(fig)
    return buf.getvalue()
