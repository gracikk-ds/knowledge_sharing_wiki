---
title: Jensen's Inequality
type: math_concept
tags: [inequality, convexity, probability, expectation]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# Jensen's Inequality

> For a convex function $\varphi$ and a random variable $X$, $\varphi(\mathbb{E}[X]) \le \mathbb{E}[\varphi(X)]$. For concave $\varphi$ the inequality flips. Equality holds iff $\varphi$ is affine on the support of $X$, or $X$ is almost-surely constant.

## Plain-English statement

We want to relate two quantities: $\varphi(\mathbb{E}[X])$ — apply $\varphi$ to the mean of $X$ — and $\mathbb{E}[\varphi(X)]$ — average $\varphi$ over the distribution of $X$. For linear $\varphi$ these are equal: $\mathbb{E}[aX + b] = a\,\mathbb{E}[X] + b$, expectation commutes with $\varphi$ and there is nothing to say. The interesting case is when $\varphi$ is nonlinear. The naive instinct is to pull $\varphi$ inside or outside the expectation as if it were linear, but for nonlinear $\varphi$ the two quantities disagree, and the disagreement has a sign.

Jensen's inequality pins down that sign. For convex $\varphi$, $\mathbb{E}[\varphi(X)] \ge \varphi(\mathbb{E}[X])$ — the average of the outputs is at least the output at the average. Convex functions curve upward, so spread in $X$ pushes $\mathbb{E}[\varphi(X)]$ above $\varphi(\mathbb{E}[X])$; a point mass closes the gap, more spread widens it.

The simplest two-point case is already informative. For $X$ taking values $a, b$ with probabilities $\lambda, 1 - \lambda$ and a convex $\varphi$, the inequality reduces to the definition of convexity:

$$
\varphi\!\big(\lambda a + (1 - \lambda) b\big) \;\le\; \lambda\,\varphi(a) + (1 - \lambda)\,\varphi(b).
$$

Jensen's inequality is the same statement extended to arbitrary distributions: the mean of $X$ on the left, the expectation of $\varphi(X)$ on the right.

For concave $\varphi$ (like $\log$), the curvature flips and so does the inequality:

$$
\varphi(\mathbb{E}[X]) \;\ge\; \mathbb{E}[\varphi(X)].
$$

This is the form used to derive the [[ml_concepts/elbo|ELBO]]: the move $\log \mathbb{E}_q[\,\cdot\,] \ge \mathbb{E}_q[\log\,\cdot\,]$ is Jensen's with concave $\log$, and the direction matters — it gives a *lower* bound on the log-evidence, which is what makes the bound usable as a training objective.

## Step-by-step proof

The cleanest proof uses the **supporting hyperplane** characterisation of convex functions.

Let $\varphi$ be convex on an interval containing the support of $X$. Set $\mu = \mathbb{E}[X]$. By convexity, there is an affine lower bound through $(\mu, \varphi(\mu))$ — a "supporting line" with slope $m$ for some $m$ (the right derivative if $\varphi$ is non-smooth, the derivative if smooth):

$$
\varphi(x) \;\ge\; \varphi(\mu) + m\,(x - \mu) \qquad \text{for all } x \text{ in the support of } X. \tag{1}
$$

Take expectation of both sides under the distribution of $X$. The right-hand side is linear in $x$, so the expectation passes inside:

$$
\mathbb{E}[\varphi(X)] \;\ge\; \varphi(\mu) + m\,(\mathbb{E}[X] - \mu) \;=\; \varphi(\mu) + 0 \;=\; \varphi(\mathbb{E}[X]).
$$

That is Jensen's inequality. Equality in (1) holds only where the support of $X$ sits on the supporting line, so equality in Jensen's holds iff $\varphi$ is affine on the support of $X$ (or $X$ is constant).

For concave $\varphi$, apply the convex result to $-\varphi$ and flip the sign.

## Geometric reading

Picture the graph of $\varphi$ and a chord between $(a, \varphi(a))$ and $(b, \varphi(b))$. For convex $\varphi$ the chord lies above the graph; for concave, below. Jensen extends this from two points to any distribution: the chord becomes the expected value $\mathbb{E}[\varphi(X)]$, and the position on the graph at $\mu = \mathbb{E}[X]$ is $\varphi(\mu)$. Convex curves trap the chord above; concave curves trap it below. Spread of $X$ widens the gap; a point mass closes it.

## Worked example

Take $X$ uniform on $\{1, 4\}$ and $\varphi(x) = x^2$ (convex).

- $\mathbb{E}[X] = 2.5$, so $\varphi(\mathbb{E}[X]) = 2.5^2 = 6.25$.
- $\mathbb{E}[\varphi(X)] = \tfrac{1}{2}(1^2 + 4^2) = \tfrac{17}{2} = 8.5$.

Jensen: $6.25 \le 8.5$ ✓. The gap is $8.5 - 6.25 = 2.25$, which equals $\mathrm{Var}(X) = \tfrac{1}{2}(1 - 2.5)^2 + \tfrac{1}{2}(4 - 2.5)^2 = 2.25$ — for $\varphi(x) = x^2$ the Jensen gap is exactly the variance.

Now the concave case: $\varphi(x) = \log x$, with $X$ uniform on $\{1, 4\}$.

- $\log \mathbb{E}[X] = \log 2.5 \approx 0.916$.
- $\mathbb{E}[\log X] = \tfrac{1}{2}(\log 1 + \log 4) = \tfrac{1}{2} \log 4 \approx 0.693$.

Jensen (concave): $0.916 \ge 0.693$ ✓. This is the AM–GM inequality in disguise: the geometric mean $\sqrt{1 \cdot 4} = 2$ is less than the arithmetic mean $2.5$, equivalently $\log$ of GM is less than $\log$ of AM, equivalently $\mathbb{E}[\log X] \le \log \mathbb{E}[X]$.

## Where it shows up in ML

- [[ml_concepts/elbo]] — derivation $\log \mathbb{E}_q[p(x, z)/q(z)] \ge \mathbb{E}_q[\log p(x, z)/q(z)]$ uses Jensen on the concave $\log$.
- [[math_concepts/kl-divergence]] — the non-negativity proof $\mathrm{KL}(q \,\|\, p) \ge 0$ uses Jensen.
- **Mutual information bounds**, **log-sum-exp** bounds, and **information-theoretic inequalities** generally — Jensen is the elementary building block.

## Common pitfalls

- **Direction of the inequality.** $\le$ for convex, $\ge$ for concave. A common bug is to derive the wrong direction by misremembering whether $\log$ is convex or concave (it is concave).
- **Strict vs non-strict.** "$\ge$" is the standard statement. Strict inequality requires $\varphi$ strictly convex on the support and $X$ non-degenerate.
- **Function vs random variable.** $\varphi$ is the function (deterministic); $X$ is the random variable. Mixing the arguments — e.g. writing $\mathbb{E}[\varphi(\mu)]$ or $\varphi(\mathbb{E}[\varphi(X)])$ — is a common source of confusion.
- **Conditional Jensen.** Jensen also applies under conditional expectation: $\varphi(\mathbb{E}[X \mid \mathcal{F}]) \le \mathbb{E}[\varphi(X) \mid \mathcal{F}]$ for convex $\varphi$. Useful in iterated-expectation arguments.

## Sources

- [[sources/elbo-and-vae-lecture]] — applies Jensen with concave $\log$ to derive the ELBO lower bound.
