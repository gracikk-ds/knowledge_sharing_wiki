"""Generates softmax-saturation.png for wiki/papers/vaswani-2017-attention-is-all-you-need.md.

Two panels:
  left  — empirical distribution of q.k for q,k ~ N(0, I_d) at d = 4, 64, 1024;
  right — entropy of softmax(scores) and softmax(scores / sqrt(d)) across d,
          where 'scores' is a row of 64 dot products against a fixed query.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent / "softmax-saturation.png"
RNG = np.random.default_rng(0)


def dot_product_samples(d: int, n: int = 20000) -> np.ndarray:
    q = RNG.standard_normal((n, d))
    k = RNG.standard_normal((n, d))
    return np.einsum("ij,ij->i", q, k)


def softmax(x: np.ndarray) -> np.ndarray:
    x = x - x.max(axis=-1, keepdims=True)
    e = np.exp(x)
    return e / e.sum(axis=-1, keepdims=True)


def entropy_bits(p: np.ndarray) -> float:
    p = np.clip(p, 1e-12, 1.0)
    return float(-(p * np.log2(p)).sum(axis=-1).mean())


def main() -> None:
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(10, 4), dpi=110)

    # left panel: distribution of q.k for several d
    dims_left = [4, 64, 1024]
    colors = ["#3b82f6", "#f59e0b", "#ef4444"]
    for d, color in zip(dims_left, colors):
        samples = dot_product_samples(d)
        ax_left.hist(
            samples,
            bins=80,
            range=(-120, 120),
            density=True,
            histtype="step",
            linewidth=1.8,
            color=color,
            label=f"d_k = {d} (std≈{samples.std():.1f})",
        )
    ax_left.set_xlabel("q · k")
    ax_left.set_ylabel("density")
    ax_left.set_title("Распределение q·k растёт как √d_k")
    ax_left.legend(loc="upper right", fontsize=9)
    ax_left.grid(alpha=0.25)

    # right panel: softmax entropy vs d, with and without 1/sqrt(d) scaling
    n_keys = 64
    dims_right = np.array([2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048])
    n_trials = 400

    ent_raw = []
    ent_scaled = []
    for d in dims_right:
        q = RNG.standard_normal((n_trials, d))
        k = RNG.standard_normal((n_trials, n_keys, d))
        scores = np.einsum("nd,nkd->nk", q, k)
        ent_raw.append(entropy_bits(softmax(scores)))
        ent_scaled.append(entropy_bits(softmax(scores / np.sqrt(d))))

    uniform_entropy = np.log2(n_keys)
    ax_right.axhline(
        uniform_entropy,
        color="#6b7280",
        linestyle=":",
        linewidth=1.2,
        label=f"равномерное по {n_keys} ключам = {uniform_entropy:.1f} бит",
    )
    ax_right.semilogx(
        dims_right,
        ent_raw,
        marker="o",
        color="#ef4444",
        label="без скейлинга: softmax(QKᵀ)",
    )
    ax_right.semilogx(
        dims_right,
        ent_scaled,
        marker="o",
        color="#3b82f6",
        label="со скейлингом: softmax(QKᵀ / √d_k)",
    )
    ax_right.set_xlabel("d_k (log scale)")
    ax_right.set_ylabel("энтропия softmax, бит")
    ax_right.set_title("Без скейлинга softmax схлопывается в почти one-hot")
    ax_right.legend(loc="lower left", fontsize=9)
    ax_right.grid(alpha=0.25, which="both")

    fig.tight_layout()
    fig.savefig(OUT, dpi=110, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
