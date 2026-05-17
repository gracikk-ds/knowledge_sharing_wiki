"""Generates attention-mask-pattern.png for wiki/papers/vaswani-2017-attention-is-all-you-need.md.

Side-by-side heatmaps showing attention weights for the same Q and K
without and with the causal mask. The figure makes the «upper triangle
becomes -inf before softmax => zero weight after softmax» mechanic
concrete: same model, same scores, two different gating policies.

Left panel — encoder self-attention: every position attends to every
position (full square has non-zero weights).

Right panel — decoder masked self-attention: position i only attends to
positions 1..i (lower-triangular weights only; everything above the
diagonal is exactly 0).
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent / "attention-mask-pattern.png"
RNG = np.random.default_rng(42)


def softmax(x: np.ndarray) -> np.ndarray:
    x = x - x.max(axis=-1, keepdims=True)
    e = np.exp(x)
    return e / e.sum(axis=-1, keepdims=True)


def main() -> None:
    n_tokens, d_k = 12, 8
    q = RNG.standard_normal((n_tokens, d_k))
    k = RNG.standard_normal((n_tokens, d_k))
    scores = q @ k.T / np.sqrt(d_k)

    weights_full = softmax(scores)

    mask = np.triu(np.ones((n_tokens, n_tokens), dtype=bool), k=1)
    scores_masked = scores.copy()
    scores_masked[mask] = -np.inf
    weights_masked = softmax(scores_masked)

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(10, 4.4), dpi=110)

    token_labels = [f"t{i}" for i in range(n_tokens)]

    for ax, weights, title in [
        (ax_left, weights_full, "Encoder self-attention\n(каждый токен видит все)"),
        (ax_right, weights_masked, "Decoder masked self-attention\n(токен i видит только 1..i)"),
    ]:
        im = ax.imshow(weights, cmap="viridis", vmin=0, vmax=weights.max(), aspect="equal")
        ax.set_xticks(range(n_tokens))
        ax.set_yticks(range(n_tokens))
        ax.set_xticklabels(token_labels, fontsize=8)
        ax.set_yticklabels(token_labels, fontsize=8)
        ax.set_xlabel("key (на что смотрим)")
        ax.set_ylabel("query (кто смотрит)")
        ax.set_title(title, fontsize=11)
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="attention weight")

    fig.suptitle("Один и тот же QK^T, две политики маскировки", fontsize=12, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT, dpi=110, bbox_inches="tight", pil_kwargs={"optimize": True})
    plt.close(fig)


if __name__ == "__main__":
    main()
