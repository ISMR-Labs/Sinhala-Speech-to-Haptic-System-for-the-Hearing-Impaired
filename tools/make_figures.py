#!/usr/bin/env python3
"""Draw the motor layout and example word patterns into docs/figures and paper/figures."""

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

from matplotlib.font_manager import FontProperties

HERE = os.path.dirname(os.path.abspath(__file__))


def sinhala_font():
    """A font that has Sinhala glyphs (macOS ships Sinhala Sangam MN; Linux: fonts-noto)."""
    import glob
    candidates = ["/System/Library/Fonts/Supplemental/Sinhala Sangam MN.ttc",
                  "/System/Library/Fonts/Sinhala Sangam MN.ttc",
                  "/Library/Fonts/Sinhala Sangam MN.ttc",
                  "/System/Library/Fonts/Supplemental/Sinhala MN.ttc"]
    candidates += glob.glob("/usr/share/fonts/**/NotoSansSinhala*.ttf", recursive=True)
    for c in candidates:
        if os.path.exists(c):
            return FontProperties(fname=c)
    return None


SI_FONT = sinhala_font()
ROOT = os.path.join(HERE, "..")
VOCAB = json.load(open(os.path.join(ROOT, "patterns", "vocabulary.json"), encoding="utf-8"))
OUTS = [os.path.join(ROOT, "docs", "figures"), os.path.join(ROOT, "paper", "figures")]

SPACING_MM = 80


def torso(ax, title, prefix, active=(), mirror=False):
    """Draw a 3x3 motor grid on a torso outline. mirror=True for the back (viewed from behind)."""
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((-150, -170), 300, 330, boxstyle="round,pad=0,rounding_size=60",
                                fc="#f2f2f2", ec="#999", lw=1.2))
    ax.plot([-60, 60], [160, 160], color="#999", lw=1.2)  # neck line
    for r in range(3):
        for c in range(3):
            i = r * 3 + c
            x = (c - 1) * SPACING_MM
            if mirror:
                x = -x
            y = 60 - r * SPACING_MM
            on = i in active
            ax.add_patch(Circle((x, y), 17, fc="#e74c3c" if on else "white", ec="#333", lw=1.4))
            ax.text(x, y, f"{prefix}{i + 1}", ha="center", va="center", fontsize=9,
                    color="white" if on else "#333", fontweight="bold")
    ax.set_xlim(-170, 170)
    ax.set_ylim(-190, 215)
    ax.text(0, 195, title, ha="center", va="bottom", fontsize=10)


def layout_figure():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 4.2))
    torso(axes[0], "Front (worn, wearer's left on the left)", "F")
    torso(axes[1], "Back (seen from behind)", "B", mirror=False)
    fig.text(0.5, 0.02, f"18 vibration modules, {SPACING_MM} mm pitch, 3 x 3 on the chest and 3 x 3 on the upper back",
             ha="center", fontsize=9, color="#444")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    return fig


def pattern_sheet(words, cols=4):
    rows = (len(words) + cols - 1) // cols
    fig = plt.figure(figsize=(2.6 * cols, 1.55 * rows))
    for k, w in enumerate(words):
        for j, fr in enumerate(w["frames"]):
            ax = fig.add_subplot(rows, cols * 2, k * 2 + j + 1)
            ax.set_aspect("equal")
            ax.axis("off")
            front = [i for i in fr["on"] if i < 9]
            back = [i - 9 for i in fr["on"] if i >= 9]
            for side, (ox, act) in enumerate(((0, front), (3.6, back))):
                ax.add_patch(FancyBboxPatch((ox - 0.5, -0.5), 3, 3, boxstyle="round,pad=0.05",
                                            fc="#f7f7f7", ec="#bbb", lw=0.8))
                for r in range(3):
                    for c in range(3):
                        i = r * 3 + c
                        on = i in act
                        ax.add_patch(Circle((ox + c, 2 - r), 0.33, fc="#e74c3c" if on else "white",
                                            ec="#555", lw=0.7))
                ax.text(ox + 1, -0.95, "front" if side == 0 else "back", ha="center", fontsize=6, color="#666")
            ax.set_xlim(-0.8, 6.8)
            ax.set_ylim(-1.3, 2.9)
            if j == 0:
                if SI_FONT is not None:
                    ax.set_title(f"{w['sinhala']}  ({w['english']})", fontsize=8, loc="left", fontproperties=SI_FONT)
                else:
                    ax.set_title(f"{w['romanised']}  ({w['english']})", fontsize=8, loc="left")
            ax.text(6.6, 2.7, f"frame {j + 1}", ha="right", fontsize=6, color="#666")
    fig.tight_layout()
    return fig


def main():
    for out in OUTS:
        os.makedirs(out, exist_ok=True)
    f1 = layout_figure()
    f2 = pattern_sheet(VOCAB["words"][:8])
    f3 = pattern_sheet(VOCAB["words"], cols=4)
    for out in OUTS:
        f1.savefig(os.path.join(out, "motor-layout.png"), dpi=200)
        f2.savefig(os.path.join(out, "patterns-example.png"), dpi=200)
    f3.savefig(os.path.join(OUTS[0], "patterns-all.png"), dpi=170)
    print("figures written")


if __name__ == "__main__":
    main()
