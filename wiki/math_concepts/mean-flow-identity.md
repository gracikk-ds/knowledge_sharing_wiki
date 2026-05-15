---
title: Mean Flow Identity
type: math_concept
tags: [generative-models, flow-map, ode, calculus]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# Mean Flow Identity

> An algebraic identity that expresses the **average** of a velocity field over an interval as the *instantaneous* velocity at the left endpoint plus a correction proportional to the time derivative of the average.

## Plain-English statement

We want a flow map $F(x_t, t, s)$ that, given a point $x_t$ at time $t$, jumps directly to time $s$ in one shot — that is what makes few-step generation possible. The natural training target for $F$ is the *average velocity* over $[t, s]$ along the trajectory:

$$
F(x_t, t, s) \;=\; \frac{1}{s - t}\int_t^s v(x_u, u)\,\mathrm{d}u,
$$

where $v(x, t)$ is the velocity of an ODE $\mathrm{d}x/\mathrm{d}u = v(x, u)$. The problem is immediate: this target is defined by an integral along the trajectory. Computing it requires integrating the ODE — which is exactly what we are trying to avoid by learning $F$ in the first place. Supervising with Monte Carlo samples of the integrand also fails: each sample $v(x_u, u)$ requires actually simulating the trajectory to time $u$, so the cost per training step scales with the number of integration steps we are trying to eliminate.

The Mean Flow Identity is the way out. It rewrites the average velocity as a purely *local* expression in $F$ and $v$:

$$
F(x_t, t, s) \;=\; v(x_t, t) \;-\; (s - t)\,\frac{\mathrm{d}}{\mathrm{d}t}F(x_t, t, s).
$$

The average velocity equals the instantaneous velocity at $t$ minus $(s - t)$ times the rate at which the average is changing in $t$. The integral is gone; what remains is the instantaneous velocity (one forward pass through a velocity model) and a total derivative of $F$ in $t$ (one Jacobian-vector product through $F_\theta$). This is the backbone of [[methods/mean-flow]]: a single network outputs $F$, and the RHS — built from $v$ and a JVP of $F$ — supervises it.

## Step-by-step derivation

Start from the definition multiplied through by $(s - t)$:

$$
(s - t)\,F(x_t, t, s) \;=\; \int_t^s v(x_u, u)\,\mathrm{d}u. \tag{1}
$$

Both sides are functions of $t$ (with $s$ held fixed and $x_t$ evolving along the trajectory). Differentiate (1) with respect to $t$.

**LHS.** Product rule:

$$
\frac{\mathrm{d}}{\mathrm{d}t}\big[(s - t)\,F\big] \;=\; (-1) \cdot F \;+\; (s - t) \cdot \frac{\mathrm{d}F}{\mathrm{d}t}.
$$

**RHS.** Leibniz rule for an integral whose lower limit moves:

$$
\frac{\mathrm{d}}{\mathrm{d}t}\int_t^s v(x_u, u)\,\mathrm{d}u \;=\; -\,v(x_t, t).
$$

(The upper limit $s$ does not depend on $t$. The lower limit contributes a minus sign because it is the *lower* limit, and the integrand evaluated there is $v(x_t, t)$.)

Equating:

$$
-F + (s - t)\frac{\mathrm{d}F}{\mathrm{d}t} \;=\; -v(x_t, t).
$$

Rearrange:

$$
F(x_t, t, s) \;=\; v(x_t, t) \;-\; (s - t)\,\frac{\mathrm{d}F}{\mathrm{d}t}.
$$

That is the Mean Flow Identity. The $\mathrm{d}/\mathrm{d}t$ on the RHS is the **total** derivative along the trajectory, so by the chain rule

$$
\frac{\mathrm{d}F}{\mathrm{d}t} \;=\; \partial_t F(x_t, t, s) \;+\; \nabla_{x_t} F(x_t, t, s) \cdot \frac{\mathrm{d}x_t}{\mathrm{d}t} \;=\; \partial_t F \;+\; (\nabla_{x_t} F) \cdot v(x_t, t). \tag{2}
$$

This is the form actually computed in code: one Jacobian-vector product through $F_\theta$ in the direction $v(x_t, t)$, plus the partial in $t$.

## Worked example

Take a one-dimensional ODE $\mathrm{d}x/\mathrm{d}u = v(x, u) = -x$. The exact solution from $(x_t, t)$ is $x_u = x_t\,e^{-(u - t)}$, so

$$
v(x_u, u) \;=\; -\,x_u \;=\; -\,x_t\,e^{-(u - t)}.
$$

Compute the integral:

$$
\int_t^s v(x_u, u)\,\mathrm{d}u \;=\; -x_t \int_t^s e^{-(u - t)}\,\mathrm{d}u \;=\; -x_t\big(1 - e^{-(s - t)}\big).
$$

So

$$
F(x_t, t, s) \;=\; \frac{-x_t\big(1 - e^{-(s - t)}\big)}{s - t}.
$$

Let $\Delta = s - t$. Then $F = -x_t (1 - e^{-\Delta})/\Delta$. Check the identity at, say, $t = 0$, $s = 1$, $x_0 = 1$:

- $F(1, 0, 1) = -(1 - e^{-1}) / 1 \approx -0.632$.
- $v(1, 0) = -1$.
- $\mathrm{d}F/\mathrm{d}t$: as $t$ increases by $\mathrm{d}t$, $x_t$ changes by $v(x_t, t)\,\mathrm{d}t = -\mathrm{d}t$, and $\Delta = s - t$ decreases by $\mathrm{d}t$. By (2), $\tfrac{\mathrm{d}F}{\mathrm{d}t}\big|_{t=0} = \partial_t F + (\partial_x F)\,v$. With $F = -x(1 - e^{-(s - t)})/(s - t)$ and $s = 1$: numerically the total derivative at $t = 0$, $x = 1$ evaluates to roughly $-0.368$.

Plug in: $v - \Delta\,\mathrm{d}F/\mathrm{d}t = -1 - 1 \cdot (-0.368) = -0.632$. Matches $F$.

(Sanity check: at $\Delta \to 0$, $(1 - e^{-\Delta})/\Delta \to 1$, so $F \to -x_t = v(x_t, t)$, recovering the boundary condition $F(t, t) = v$.)

## Where it shows up in ML

- [[methods/mean-flow]] — uses the identity as a stop-gradient target so the network's flow-map output stays consistent with its flow-matching velocity head.
- [[ml_concepts/flow-map]] — the broader concept the identity supports.

## Common pitfalls

- **Total vs partial derivative.** $\mathrm{d}/\mathrm{d}t$ in the identity is the total derivative along the trajectory, which includes the convective term $(\nabla_x F) \cdot v$. Using only $\partial_t F$ drops the dominant piece in most practical settings.
- **Sign on the Leibniz term.** The integral has $t$ as the **lower** limit, so differentiating gives $-v(x_t, t)$, not $+v(x_t, t)$.
- **Boundary direction.** $s > t$ is the convention here. With $s < t$ the sign of $(s - t)$ flips and so does the correction term.
- **Stop-gradient placement.** In training, only the RHS is detached; gradients flow through the LHS $F_\theta$. Detaching the LHS would block learning entirely.

## Sources

- [[sources/flow-map-models-lecture]] — states the identity in the form $F = v - (s - t)\,\mathrm{d}F/\mathrm{d}t$ and uses it as the Mean Flow training target.
