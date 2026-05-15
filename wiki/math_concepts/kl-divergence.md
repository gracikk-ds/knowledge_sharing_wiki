---
title: KL Divergence
type: math_concept
tags: [information-theory, probability, divergence, variational-inference]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# KL Divergence

> A non-negative, asymmetric measure of how much one probability distribution $q$ differs from a reference $p$, defined as $\mathrm{KL}(q \,\|\, p) = \mathbb{E}_{x \sim q}\big[\log\,q(x) / p(x)\big]$. Equals zero iff $q = p$ almost everywhere.

## Plain-English statement

We want a way to measure how much one distribution $q$ disagrees with another $p$. The naive move is to treat densities as vectors and take an $L^2$ distance, $\int (q(x) - p(x))^2\,dx$. This is well-defined but wrong-feeling for probabilities. Probabilities live on a log scale — the difference between $0.5$ and $0.51$ is mundane, the difference between $10^{-6}$ and $10^{-7}$ is a factor of ten in likelihood — and $L^2$ ignores that. It also treats the gap symmetrically, while the asymmetry between "$q$ assigns mass where $p$ does not" and "$p$ assigns mass where $q$ does not" actually matters in coding and in likelihood.

KL divergence fixes the scale problem by using the log-ratio $\log\,q(x)/p(x)$ as the integrand, and averages it under $q$ — the distribution we are comparing *from*. The result is non-negative, zero only when $q = p$, and intrinsically asymmetric: $\mathrm{KL}(q \,\|\, p) \ne \mathrm{KL}(p \,\|\, q)$ in general, and the triangle inequality does not hold. The asymmetry is what makes it useful — in maximum likelihood the "from" distribution is the data; in variational inference it is the proposal.

The same quantity has a coding-theory reading: $\mathrm{KL}(q \,\|\, p)$ is the expected extra log-probability you pay per sample from $q$ if you encode using a code optimal for $p$ rather than for $q$. Same formula, different motivation.

For discrete $q, p$ on the same support:

$$
\mathrm{KL}(q \,\|\, p) \;=\; \sum_x q(x)\,\log \frac{q(x)}{p(x)}.
$$

For continuous distributions with densities $q(x), p(x)$:

$$
\mathrm{KL}(q \,\|\, p) \;=\; \int q(x)\,\log \frac{q(x)}{p(x)}\,dx.
$$

Either form requires the support of $q$ to be contained in the support of $p$: if $p(x) = 0$ for some $x$ with $q(x) > 0$, the integrand is $+\infty$.

## Step-by-step: non-negativity

The defining property is $\mathrm{KL}(q \,\|\, p) \ge 0$, with equality iff $q = p$. Proof using [[math_concepts/jensens-inequality]]:

Start with the definition and rewrite the log:

$$
\mathrm{KL}(q \,\|\, p) \;=\; \int q(x)\,\log \frac{q(x)}{p(x)}\,dx \;=\; -\int q(x)\,\log \frac{p(x)}{q(x)}\,dx \;=\; -\,\mathbb{E}_{x \sim q}\!\Big[\log \frac{p(x)}{q(x)}\Big].
$$

Apply Jensen's inequality with concave $\log$: $\mathbb{E}[\log Y] \le \log \mathbb{E}[Y]$. Negating flips the direction:

$$
-\,\mathbb{E}_{x \sim q}\!\Big[\log \frac{p(x)}{q(x)}\Big] \;\ge\; -\log \mathbb{E}_{x \sim q}\!\Big[\frac{p(x)}{q(x)}\Big].
$$

Compute the inner expectation:

$$
\mathbb{E}_{x \sim q}\!\Big[\frac{p(x)}{q(x)}\Big] \;=\; \int q(x)\,\frac{p(x)}{q(x)}\,dx \;=\; \int p(x)\,dx \;=\; 1.
$$

So $-\log 1 = 0$ and $\mathrm{KL}(q \,\|\, p) \ge 0$. Equality holds iff Jensen's is tight, i.e. $p(x)/q(x)$ is constant almost surely under $q$. Combined with $\int p = \int q = 1$, this forces $p = q$ almost everywhere.

## Step-by-step: KL between two Gaussians

This is the form used analytically in [[methods/vae]]. Let $q = \mathcal{N}(\mu_1, \sigma_1^2)$ and $p = \mathcal{N}(\mu_2, \sigma_2^2)$ in one dimension. Then

$$
\mathrm{KL}(q \,\|\, p) \;=\; \log\frac{\sigma_2}{\sigma_1} \;+\; \frac{\sigma_1^2 + (\mu_1 - \mu_2)^2}{2\sigma_2^2} \;-\; \frac{1}{2}.
$$

Derivation. Write out the log ratio:

$$
\log \frac{q(x)}{p(x)} \;=\; \log \frac{\sigma_2}{\sigma_1} \;-\; \frac{(x - \mu_1)^2}{2\sigma_1^2} \;+\; \frac{(x - \mu_2)^2}{2\sigma_2^2}.
$$

Take the expectation under $q$. Using $\mathbb{E}_q[(x - \mu_1)^2] = \sigma_1^2$ and $\mathbb{E}_q[(x - \mu_2)^2] = \sigma_1^2 + (\mu_1 - \mu_2)^2$ (variance plus squared bias):

$$
\mathrm{KL}(q \,\|\, p) \;=\; \log\frac{\sigma_2}{\sigma_1} \;-\; \frac{\sigma_1^2}{2\sigma_1^2} \;+\; \frac{\sigma_1^2 + (\mu_1 - \mu_2)^2}{2\sigma_2^2} \;=\; \log\frac{\sigma_2}{\sigma_1} - \tfrac{1}{2} + \frac{\sigma_1^2 + (\mu_1 - \mu_2)^2}{2\sigma_2^2}.
$$

**Special case used in VAE.** With $p = \mathcal{N}(0, 1)$ (the standard prior) and $q = \mathcal{N}(\mu_1, \sigma_1^2)$, setting $\mu_2 = 0$ and $\sigma_2 = 1$:

$$
\mathrm{KL}\!\big(\mathcal{N}(\mu_1, \sigma_1^2) \,\|\, \mathcal{N}(0, 1)\big) \;=\; \tfrac{1}{2}\big(\mu_1^2 + \sigma_1^2 - \log \sigma_1^2 - 1\big).
$$

For a $d$-dimensional diagonal Gaussian $q = \mathcal{N}(\mu, \mathrm{diag}(\sigma^2))$ against standard normal prior $p = \mathcal{N}(0, I)$, the KL decomposes across coordinates:

$$
\mathrm{KL}\!\big(q \,\|\, p\big) \;=\; \tfrac{1}{2}\sum_{i=1}^d \big(\mu_i^2 + \sigma_i^2 - \log \sigma_i^2 - 1\big).
$$

This is the closed-form regulariser term in the VAE loss.

## Worked example

Take $q$ = Bernoulli($0.8$) and $p$ = Bernoulli($0.5$).

$$
\mathrm{KL}(q \,\|\, p) \;=\; 0.8\,\log \tfrac{0.8}{0.5} + 0.2\,\log\tfrac{0.2}{0.5} \;=\; 0.8\,\log 1.6 + 0.2\,\log 0.4.
$$

With natural log: $0.8 \cdot 0.470 + 0.2 \cdot (-0.916) \approx 0.376 - 0.183 \approx 0.193$ nats.

Now the other direction:

$$
\mathrm{KL}(p \,\|\, q) \;=\; 0.5\,\log \tfrac{0.5}{0.8} + 0.5\,\log\tfrac{0.5}{0.2} \;\approx\; 0.5 \cdot (-0.470) + 0.5 \cdot 0.916 \;\approx\; 0.223 \text{ nats}.
$$

Different: $0.193 \ne 0.223$. The asymmetry is real and small even for unimodal Bernoullis.

## Forward vs reverse KL

Two ways to use KL to fit one distribution to another:

- **Forward KL** $\mathrm{KL}(p \,\|\, q)$ — used in maximum-likelihood training (treat $p$ as the data distribution, $q$ as the model). Mass-covering: $q$ must cover all the support of $p$.
- **Reverse KL** $\mathrm{KL}(q \,\|\, p)$ — used in variational inference (treat $p$ as the true posterior, $q$ as the approximation). Mode-seeking: $q$ avoids putting mass where $p$ is small, often collapsing to a single mode of a multimodal $p$.

The choice often comes down to which expectation is tractable: forward KL requires sampling under $p$ (the unknown thing), reverse KL requires sampling under $q$ (the proposal we built).

## Where it shows up in ML

- [[ml_concepts/elbo]] — the gap $\log p(x) - \mathrm{ELBO}$ equals $\mathrm{KL}(q \,\|\, p(z \mid x))$.
- [[ml_concepts/variational-inference]] — VI minimises $\mathrm{KL}(q \,\|\, p(z \mid x))$, equivalently maximises ELBO.
- [[methods/vae]] — uses the closed-form Gaussian-vs-Gaussian KL as the regulariser.
- Maximum likelihood training is forward-KL minimisation: $\min_\theta \mathrm{KL}(\pi(x) \,\|\, p(x \mid \theta))$, with the data-entropy term constant.

## Common pitfalls

- **Asymmetry.** $\mathrm{KL}(q \,\|\, p) \ne \mathrm{KL}(p \,\|\, q)$ in general. Always check which direction you actually want.
- **Support.** If $p(x) = 0$ where $q(x) > 0$, KL is infinite. In practice always use a $p$ with full support, or carefully ensure $q$'s support is contained in $p$'s.
- **Base of the log.** Natural log (nats) is standard in ML; log base 2 (bits) shows up in information theory. The choice is a unit, not a different quantity, but the numerical values differ.
- **KL is not a distance.** No triangle inequality, asymmetric. Use Jensen-Shannon divergence or Wasserstein if you need a metric.
- **Sign error on the Gaussian formula.** A common bug is $-\log\sigma_1^2$ vs $+\log\sigma_1^2$. The correct sign in the formula above is $-\log\sigma_1^2$ — the term penalises *small* $\sigma_1$ (over-confidence) more strongly. Easy to verify numerically with $\mu_1 = 0, \sigma_1 = 1$ giving $\mathrm{KL} = 0$.

## Sources

- [[sources/elbo-and-vae-lecture]] — uses KL throughout: as the forward-KL loss to minimise, the gap term in the ELBO identity, the regulariser term in the VAE loss, and the closed-form Gaussian-to-Gaussian expression.
