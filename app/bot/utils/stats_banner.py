import io
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patches import FancyBboxPatch

BG = "#16161e"
FG = "#e6e6ef"
MUTED = "#8b8b9e"

ICONS_DIR = Path(__file__).resolve().parents[3] / "assets" / "engine_icons"

ENGINE_COLORS = {
    "deezer": "#a238ff",
    "soundcloud": "#ff5500",
    "youtube": "#ff0000",
    "spotify": "#1ed760",
    "yandex": "#fc3f1d",
}


def _render_banner(
        data: dict[str, int],
        title: str,
        colors: dict[str, str] | None = None,
        icons: bool = False
) -> bytes:
    sns.set_theme(style="dark")
    items = sorted(data.items(), key=lambda kv: -kv[1])
    labels = [k for k, _ in items]
    values = [v for _, v in items]
    total = sum(values)

    if colors:
        wedge_colors = [colors.get(l, "#5b6270") for l in labels]
    else:
        wedge_colors = sns.color_palette("muted", n_colors=max(len(labels), 3)).as_hex()[:len(labels)]

    fig = plt.figure(figsize=(10.8, 8.1), facecolor=BG)
    ax_pie = fig.add_axes((0.02, 0.08, 0.5, 0.78))
    ax_leg = fig.add_axes((0.54, 0.08, 0.44, 0.78))
    for ax in (ax_pie, ax_leg):
        ax.set_facecolor(BG)
        ax.axis("off")

    ax_pie.pie(
        values,
        colors=wedge_colors,
        startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.42, "edgecolor": BG, "linewidth": 2},
    )
    ax_pie.text(0, 0, f"{total}", ha="center", va="center",
                color=FG, fontsize=30, fontweight="bold")

    ax_leg.set_xlim(0, 1)
    ax_leg.set_ylim(0, 1)
    row_h = min(0.16, 0.9 / max(len(items), 1))
    y0 = 0.5 + row_h * (len(items) - 1) / 2
    for i, (label, value) in enumerate(items):
        y = y0 - i * row_h
        icon_path = ICONS_DIR / f"{label}.png" if icons else None
        if icon_path and icon_path.exists():
            img = plt.imread(icon_path)
            ab = AnnotationBbox(
                OffsetImage(img, zoom=0.32),
                (0.06, y), xycoords=ax_leg.transAxes,
                frameon=False
            )
            ax_leg.add_artist(ab)
        else:
            ax_leg.add_patch(FancyBboxPatch(
                (0.03, y - 0.028), 0.056, 0.056,
                boxstyle="round,pad=0.004,rounding_size=0.012",
                linewidth=0, facecolor=wedge_colors[i],
                transform=ax_leg.transAxes
            ))
        text_x = 0.16
        pct = f"{value / total * 100:.0f}%" if total else "0%"
        ax_leg.text(text_x, y, label, ha="left", va="center",
                    color=FG, fontsize=18, fontweight="bold")
        ax_leg.text(0.98, y, f"{value}  ({pct})", ha="right", va="center",
                    color=MUTED, fontsize=16)

    fig.text(0.04, 0.93, title, color=FG, fontsize=21, fontweight="bold")
    fig.text(0.04, 0.03, "koshke usage stats", color=MUTED, fontsize=11)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, facecolor=BG)
    plt.close(fig)
    return buf.getvalue()


def render_engine_banner(by_engine: dict[str, int]) -> bytes:
    return _render_banner(by_engine, "downloads by engine", colors=ENGINE_COLORS, icons=True)


def render_context_banner(by_context: dict[str, int]) -> bytes:
    return _render_banner(by_context, "downloads by context")
