"""Generates path-length-vs-n.png for wiki/papers/vaswani-2017-attention-is-all-you-need.md.

Reproduces the «Max path length» column from Table 1 visually:
how many sequential ops the gradient signal traverses from the first input
token to the last output token as a function of sequence length n, for each
layer family. The point of the figure is to make «O(1) path length for
self-attention» a concrete number, not an asymptotic claim.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent / "path-length-vs-n.png"


def main() -> None:
    n = np.arange(2, 4097)
    k = 3  # convolutional kernel width assumed

    self_attn = np.ones_like(n, dtype=float)
    bytenet = np.log(n) / np.log(k)
    convs2s = n / k
    rnn = n.astype(float)

    fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=120)
    ax.plot(n, rnn, color="#ef4444", lw=2.0, label="RNN / LSTM — O(n)")
    ax.plot(n, convs2s, color="#f59e0b", lw=2.0, label=f"ConvS2S (k={k}) — O(n/k)")
    ax.plot(n, bytenet, color="#10b981", lw=2.0, label=f"ByteNet (k={k}) — O(log_k n)")
    ax.plot(n, self_attn, color="#3b82f6", lw=2.5, label="Self-attention — O(1)")

    pivot = 50
    annotations = [
        (pivot, pivot, "RNN: 50", "#ef4444", (8, 8)),
        (pivot, pivot / k, f"ConvS2S: ~{pivot // k}", "#f59e0b", (8, -4)),
        (pivot, np.log(pivot) / np.log(k), f"ByteNet: ~{int(round(np.log(pivot) / np.log(k)))}", "#10b981", (8, -12)),
        (pivot, 1.0, "Self-attention: 1", "#3b82f6", (8, -20)),
    ]
    for x, y, text, color, offset in annotations:
        ax.scatter([x], [y], color=color, zorder=5, s=40)
        ax.annotate(
            text,
            xy=(x, y),
            xytext=offset,
            textcoords="offset points",
            color=color,
            fontsize=9,
            fontweight="bold",
        )
    ax.axvline(pivot, color="#9ca3af", ls=":", lw=0.8)
    ax.annotate(
        "типичная длина\nпредложения в NMT",
        xy=(pivot, 0.4),
        xytext=(70, 0.45),
        fontsize=8,
        color="#6b7280",
    )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("длина последовательности n (log)")
    ax.set_ylabel("длина пути — число последовательных операций (log)")
    ax.set_title("Длина пути от первого ко последнему токену vs длина последовательности")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(alpha=0.25, which="both")
    ax.set_xlim(2, 4096)
    ax.set_ylim(0.7, 5000)

    fig.tight_layout()
    fig.savefig(OUT, dpi=120, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
