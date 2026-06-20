# ML Notes Wiki

This directory is a personal wiki for building structured understanding of machine learning.

---
### Line length

Do **not** manually wrap prose. Obsidian soft-wraps text at display time, so source-level line breaks inside a paragraph just clutter diffs and have no rendering effect.
### Math notation

All mathematical notation goes in **LaTeX**, never in backticks. Inline math uses `$...$`, display math uses `$$...$$`. This applies to symbols, expressions, equations, set notation, function notation — anything mathematical, even a single Greek letter or a single subscripted variable. Backticks are reserved for code identifiers (function names, module paths, parameter names, type names, file paths, library names).

Bad (math notation in backticks):

- `t_0 < t_1 < ... < t_N`
- `s, t ∈ [0,σ]`
- `f_θ(x, t) = c_skip(t)·x + c_out(t)·F_θ(x, t)`
- `{x_τ}_{τ ∈ [0,σ]}`
- `x_0`, `f_θ`, `Δ = s - t`

Good (LaTeX):

- $t_0 < t_1 < \ldots < t_N$
- $s, t \in [0, \sigma]$
- $f_\theta(x, t) = c_{\text{skip}}(t) \cdot x + c_{\text{out}}(t) \cdot F_\theta(x, t)$
- $\{x_\tau\}_{\tau \in [0, \sigma]}$
- $x_0$, $f_\theta$, $\Delta = s - t$

In Unicode-clean math expressions (e.g. `σ`, `θ`, `·`, `∈`, `≤`, `→`) inside backticks, convert to LaTeX commands (`\sigma`, `\theta`, `\cdot`, `\in`, `\leq`, `\to`). Multi-letter subscripts like `skip` or `out` use `_{\text{...}}` for upright font; single-letter subscripts go bare (`x_t`, `f_\theta`).
