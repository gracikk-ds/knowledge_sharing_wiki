---
title: How is the Mean Flow time-derivative dF/dt computed in practice?
type: question
tags: [mean-flow, flow-map, jvp, autograd]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: stub
---

# How is the Mean Flow time-derivative $\mathrm{d}F/\mathrm{d}t$ computed in practice?

## Why it matters

The [[math_concepts/mean-flow-identity]] uses $\tfrac{\mathrm{d}}{\mathrm{d}t} F_\theta(x_t, t, s)$ as its supervision signal. This is a *total* derivative along the trajectory:

$$
\frac{\mathrm{d}}{\mathrm{d}t} F_\theta(x_t, t, s) \;=\; \partial_t F_\theta \;+\; (\nabla_x F_\theta)\,v(x_t, t).
$$

To train Mean Flow you need this quantity for every sample at every step. The implementation matters: a naive autograd-over-autograd would be expensive.

## What we know so far

- The right tool is a **forward-mode Jacobian-vector product (JVP)** through $F_\theta$ in the direction $v(x_t, t)$, with the $t$ argument carrying its own tangent of $1$. One JVP yields both $\partial_t F$ and $(\nabla_x F) \cdot v$ simultaneously.
- In PyTorch: `torch.func.jvp(lambda x, t: F(x, t, s), (x_t, t), (v, ones))`.
- Cost: roughly one forward pass through $F_\theta$ (forward-mode AD is cheap when there is only one tangent direction).

## What would resolve it

- A complete training-loop reference implementation showing JVP usage, loss bookkeeping, and stop-gradient placement.
- Confirmation from the original Mean Flow paper (Geng et al. 2025) that the JVP route is what they use, vs. some surrogate.

## Related

- [[methods/mean-flow]]
- [[math_concepts/mean-flow-identity]]
- [[sources/flow-map-models-lecture]]
