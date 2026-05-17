"""Generates positional-encoding-pattern.png for wiki/papers/vaswani-2017-attention-is-all-you-need.md.

Shows the sinusoidal positional encoding as a heatmap: row = position in
the sequence (0..127), column = embedding dimension (0..127), colour = PE
value in [-1, 1]. The point is to make the «low-dim => high frequency,
high-dim => low frequency» pattern visually obvious — and to show why two
nearby positions get similar PE vectors (rows differ slowly), while two
distant positions get visibly different ones.

A second panel plots PE rows for three fixed positions (10, 40, 70) over
all dimensions so the per-position vector is recognisable.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent / "positional-encoding-pattern.png"


def positional_encoding(n_positions: int, d_model: int) -> np.ndarray:
    pe = np.zeros((n_positions, d_model))
    position = np.arange(n_positions)[:, None]
    div = np.exp(np.arange(0, d_model, 2) * -(np.log(10000.0) / d_model))
    pe[:, 0::2] = np.sin(position * div)
    pe[:, 1::2] = np.cos(position * div)
    return pe


def main() -> None:
    n_pos, d_model = 96, 96
    pe = positional_encoding(n_pos, d_model)

    fig, (ax_heatmap, ax_curves) = plt.subplots(
        1, 2, figsize=(9, 3.8), dpi=96, gridspec_kw={"width_ratios": [1.0, 1.0]}
    )

    im = ax_heatmap.imshow(
        pe, aspect="auto", cmap="RdBu_r", vmin=-1, vmax=1, interpolation="nearest"
    )
    ax_heatmap.set_xlabel("размерность эмбеддинга i (0..95)")
    ax_heatmap.set_ylabel("позиция pos (0..95)")
    ax_heatmap.set_title("Sinusoidal PE: тепловая карта PE[pos, i]")
    fig.colorbar(im, ax=ax_heatmap, fraction=0.046, pad=0.04, label="PE value")

    sample_positions = [10, 40, 80]
    colors = ["#3b82f6", "#10b981", "#ef4444"]
    for pos, color in zip(sample_positions, colors):
        ax_curves.plot(pe[pos], color=color, lw=1.4, label=f"pos = {pos}")
    ax_curves.set_xlabel("размерность эмбеддинга i")
    ax_curves.set_ylabel("PE[pos, i]")
    ax_curves.set_title("PE-вектор для трёх позиций")
    ax_curves.legend(loc="upper right", fontsize=9)
    ax_curves.grid(alpha=0.25)
    ax_curves.set_ylim(-1.15, 1.15)

    fig.tight_layout()
    fig.savefig(OUT, dpi=96, bbox_inches="tight", pil_kwargs={"optimize": True})
    plt.close(fig)


if __name__ == "__main__":
    main()
