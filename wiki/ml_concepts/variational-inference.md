---
title: Variational Inference
type: ml_concept
tags: [variational-inference, latent-variable-models, generative-models, probabilistic-modelling]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# Variational Inference

> A framework for approximating an intractable posterior $p(z \mid x, \theta)$ by an easier distribution $q(z)$ chosen from a tractable family, with the approximation quality measured by $\mathrm{KL}(q \,\|\, p(z \mid x, \theta))$.

## Motivation

In a [[ml_concepts/latent-variable-model]] we keep needing the posterior $p(z \mid x, \theta)$ — for predictions, for evaluating expectations that show up in training objectives, for analysing what the model has learned. Bayes' rule writes it down:

$$
p(z \mid x, \theta) \;=\; \frac{p(x \mid z, \theta)\,p(z)}{p(x \mid \theta)}.
$$

The denominator is the marginal likelihood, the same integral we already cannot compute. So the posterior is known up to a normaliser we have no way to evaluate. Plugging in MCMC samples is one route but is slow, mixes poorly in high dimensions, and is hard to amortise across many examples.

Variational inference replaces inference with optimisation. Pick a tractable family $\mathcal{Q} = \{q\}$ — diagonal Gaussians, mean-field factorisations, more elaborate parametric families — and search within it for the $q$ closest to the true posterior, measured by [[math_concepts/kl-divergence]]. The chosen $q^*$ is then used as a proxy: expectations under the true posterior get replaced by expectations under $q^*$, which we can compute because $q^*$ was picked from a tractable family.

A direct attempt to minimise $\mathrm{KL}(q \,\|\, p(z \mid x, \theta))$ runs into the same wall as before, because the KL contains $\log p(z \mid x, \theta)$ and that requires the same unknown normaliser. The workaround is the identity $\log p(x \mid \theta) = \mathrm{ELBO}(q, \theta) + \mathrm{KL}(q \,\|\, p(z \mid x, \theta))$. The left-hand side does not depend on $q$, so minimising the KL over $q$ is exactly the same problem as maximising the [[ml_concepts/elbo|ELBO]] over $q$. The ELBO needs only the joint $p(x, z \mid \theta) = p(x \mid z, \theta)\,p(z)$, which we have. This is the foundational move of VI: the intractable objective and a tractable surrogate differ by a constant in $q$, so optimising the surrogate is equivalent to optimising the real thing.

The remaining design choice is the family $\mathcal{Q}$. A richer family lands closer to the true posterior but harder to optimise, with higher-variance gradient estimators. Mean-field $q(z) = \prod_j q_j(z_j)$ is the classical default; diagonal Gaussians dominate amortised settings. This trade-off — bias from $\mathcal{Q}$ versus optimisation cost — is the main knob a VI practitioner turns.

## Formal description

For fixed $x$ and $\theta$, VI solves

$$
q^* \;=\; \arg\min_{q \in \mathcal{Q}}\,\mathrm{KL}\!\big(q(z) \,\|\, p(z \mid x, \theta)\big).
$$

The KL is intractable directly (it contains $\log p(z \mid x, \theta)$), but we can sidestep this using the identity

$$
\log p(x \mid \theta) \;=\; \mathrm{ELBO}(q, \theta) \;+\; \mathrm{KL}\!\big(q(z) \,\|\, p(z \mid x, \theta)\big).
$$

The left-hand side does not depend on $q$. Therefore, at fixed $\theta$:

$$
\arg\min_{q} \mathrm{KL}\!\big(q(z) \,\|\, p(z \mid x, \theta)\big) \;\equiv\; \arg\max_{q} \mathrm{ELBO}(q, \theta).
$$

So we never need the true posterior to fit $q$ — maximising the [[ml_concepts/elbo|ELBO]] over $q$ is exactly the same optimisation as minimising the KL to the posterior. This is the foundational identity of VI.

## Why reverse KL (not forward)

VI minimises $\mathrm{KL}(q \,\|\, p)$, not $\mathrm{KL}(p \,\|\, q)$. The asymmetry matters:

- $\mathrm{KL}(q \,\|\, p)$ is "mode-seeking": $q$ pays a large penalty when it puts mass where $p$ is near zero, but not vice versa. The optimiser tends to fit $q$ to one mode of a multimodal posterior.
- $\mathrm{KL}(p \,\|\, q)$ is "mass-covering": $q$ must cover all the support of $p$ to avoid blow-up. Hard to compute since expectation is under $p$.

Reverse KL is chosen because $q$ is the proposal we can sample from — expectations under $q$ are tractable. See [[math_concepts/kl-divergence]] for the asymmetry in detail.

## Choosing the family

The classical choice is the **mean-field** family: $q(z) = \prod_j q_j(z_j)$, each factor in some simple parametric family. Fully factorised, easy to sample, but cannot represent correlations between latents.

For amortised settings (one inference network for all $x$), the typical choice is the **diagonal Gaussian** $q(z \mid x, \phi) = \mathcal{N}(\mu_\phi(x), \mathrm{diag}(\sigma_\phi^2(x)))$, with $\mu_\phi, \sigma_\phi$ outputs of a neural network. This is what [[methods/vae]] uses. Richer families exist (normalising flows for $q$, structured posteriors) at additional cost.

## Variations and related concepts

- [[ml_concepts/elbo]] — the surrogate optimised in place of the intractable KL.
- [[ml_concepts/amortized-variational-inference]] — share one $q(z \mid x, \phi)$ across all examples.
- [[ml_concepts/reparameterization-trick]] — backprop through $\nabla_\phi \mathbb{E}_{q}[\cdot]$.
- [[methods/variational-em]] — alternate VI ($q$ updates) with model updates.
- [[methods/vae]] — VI parameterised end-to-end as a deep autoencoder.
- [[math_concepts/kl-divergence]] — the measure of "closeness" being minimised.

## Open questions

- {none}

## Sources

- [[sources/elbo-and-vae-lecture]] — derivation that minimising KL to the posterior is the same problem as maximising ELBO, plus the EM-style optimisation path.

## Up next

- [[ml_concepts/elbo]] — the surrogate objective that turns intractable KL minimisation into a tractable maximisation problem.
- [[ml_concepts/amortized-variational-inference]] — share one neural network across all $x$ instead of fitting $q$ per example.
