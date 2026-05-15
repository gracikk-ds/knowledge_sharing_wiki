---
title: Evidence Lower Bound (ELBO)
type: ml_concept
tags: [variational-inference, latent-variable-models, generative-models, training-objectives, vae]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# Evidence Lower Bound (ELBO)

> A tractable lower bound on the marginal log-likelihood $\log p(x \mid \theta)$ of a latent-variable model, obtained by introducing an auxiliary distribution $q(z)$ over latents. ELBO is the central training objective of variational inference and of VAEs.

## Motivation

We have a [[ml_concepts/latent-variable-model]] $p(x \mid \theta) = \int p(x \mid z, \theta)\,p(z)\,dz$. The thing we want — maximum likelihood — needs that integral. It has no closed form, so the first instinct is Monte Carlo: sample $z \sim p(z)$, average $p(x \mid z, \theta)$. This fails for a specific reason. For any one $x$, almost every prior sample lands on a $z$ that has nothing to do with it, so $p(x \mid z, \theta) \approx 0$. Out of 1000 samples maybe one contributes; the estimator has near-infinite variance.

ELBO is the workaround. Instead of $p(z)$, sample from a smarter $q(z)$ biased toward latents that could explain $x$. The quantity you can estimate this way is a *lower bound* on $\log p(x \mid \theta)$ — not the thing itself, but tight when $q$ is close to the true posterior, and that gap shrinks the more $q$ improves.

This gives the bound two readings, both load-bearing. As a Jensen's-inequality bound it holds for *any* valid $q$, so you can pick $q$ from a tractable family and still get a usable training signal. As an exact identity, $\log p(x \mid \theta) = \mathrm{ELBO}(q, \theta) + \mathrm{KL}(q(z) \,\|\, p(z \mid x, \theta))$, the gap between the bound and the true log-evidence equals the KL from $q$ to the true posterior. Equality holds when $q$ is the true posterior. This is why training a VAE jointly in $\theta$ and $q$ does two things at once: it pushes up the model's marginal likelihood and pulls $q$ toward the true posterior.

## Formal description

**Derivation via Jensen's inequality.** For any $q(z)$ positive wherever $p(x, z \mid \theta) > 0$, multiply and divide by $q(z)$ inside the integral and apply [[math_concepts/jensens-inequality]] with the concave $\log$:

$$
\log p(x \mid \theta) = \log \int q(z)\,\frac{p(x, z \mid \theta)}{q(z)}\,dz = \log\,\mathbb{E}_{z \sim q}\!\Big[\frac{p(x, z \mid \theta)}{q(z)}\Big] \ge \mathbb{E}_{z \sim q}\!\Big[\log \frac{p(x, z \mid \theta)}{q(z)}\Big]
$$

The right-hand side is the **ELBO**:

$$
\mathrm{ELBO}(q, \theta) \;=\; \mathbb{E}_{z \sim q(z)}\!\Big[\log \frac{p(x, z \mid \theta)}{q(z)}\Big].
$$

**Exact identity with the posterior gap.** Using Bayes' rule $p(x, z \mid \theta) = p(z \mid x, \theta)\,p(x \mid \theta)$:

$$
\mathrm{ELBO}(q, \theta) = \int q(z)\,\log\frac{p(z \mid x, \theta)\,p(x \mid \theta)}{q(z)}\,dz = \log p(x \mid \theta) - \mathrm{KL}\!\big(q(z) \,\|\, p(z \mid x, \theta)\big).
$$

Equivalently:

$$
\boxed{\;\log p(x \mid \theta) \;=\; \mathrm{ELBO}(q, \theta) \;+\; \mathrm{KL}\!\big(q(z) \,\|\, p(z \mid x, \theta)\big)\;}
$$

Since [[math_concepts/kl-divergence]] is non-negative, this recovers $\log p(x \mid \theta) \ge \mathrm{ELBO}(q, \theta)$ — and tells us exactly when equality holds: $q(z) = p(z \mid x, \theta)$.

**Reconstruction–regularisation decomposition.** Splitting $p(x, z \mid \theta) = p(x \mid z, \theta)\,p(z)$ gives the form used in VAEs:

$$
\mathrm{ELBO}(q, \theta) \;=\; \underbrace{\mathbb{E}_{z \sim q}\!\big[\log p(x \mid z, \theta)\big]}_{\text{reconstruction}} \;-\; \underbrace{\mathrm{KL}\!\big(q(z) \,\|\, p(z)\big)}_{\text{regularisation}}.
$$

The first term forces the decoder $p(x \mid z, \theta)$ to assign high probability to $x$ when $z$ is drawn from $q$. For a Gaussian decoder this is (up to constants) an MSE; for a Bernoulli decoder, cross-entropy. The second term keeps $q$ from drifting too far from the prior $p(z)$, which would let the model overfit by hand-picking a specific $z$ per $x$.

## Optimisation

Because $\log p(x \mid \theta) \ge \mathrm{ELBO}(q, \theta)$, maximising the bound jointly in $\theta$ and $q$ is a proxy for maximum likelihood:

$$
\max_\theta \log p(x \mid \theta) \;\Rightarrow\; \max_{\theta, q}\,\mathrm{ELBO}(q, \theta).
$$

Two paradigms:

- **[[methods/variational-em]]** — alternate: at fixed $\theta$, set $q$ to maximise ELBO (E-step); at fixed $q$, update $\theta$ (M-step). At fixed $\theta$, $\log p(x \mid \theta)$ doesn't depend on $q$, so maximising ELBO over $q$ is equivalent to minimising $\mathrm{KL}(q \,\|\, p(z \mid x, \theta))$ — i.e. fitting $q$ to the true posterior.
- **VAEs** — parameterise $q$ as $q(z \mid x, \phi)$ via [[ml_concepts/amortized-variational-inference]] (an encoder network) and update $(\phi, \theta)$ jointly by SGD. See [[methods/vae]].

The two coordinates of the gradient are handled differently:

- $\nabla_\theta \mathrm{ELBO}$: $q$ does not depend on $\theta$, so the gradient swaps with the expectation and is a plain Monte Carlo estimator.
- $\nabla_\phi \mathrm{ELBO}$: $q$ depends on $\phi$. The naïve interchange of gradient and expectation is wrong; use the [[ml_concepts/reparameterization-trick]] (or the higher-variance score-function estimator).

## Variations and related concepts

- [[ml_concepts/latent-variable-model]] — the setup that motivates ELBO.
- [[ml_concepts/variational-inference]] — the framework around ELBO.
- [[ml_concepts/amortized-variational-inference]] — share one network across all $x$ instead of fitting $q$ per example.
- [[ml_concepts/reparameterization-trick]] — how to backprop through $\nabla_\phi \mathrm{ELBO}$.
- [[methods/vae]] — ELBO with a Gaussian amortised encoder, trained end-to-end.
- [[methods/variational-em]] — ELBO maximised by alternating $q$ and $\theta$.
- [[math_concepts/jensens-inequality]] — provides the inequality direction.
- [[math_concepts/kl-divergence]] — measures the bound's slack and appears in the regularisation term.

## Open questions

- {none surfaced yet}

## Sources

- [[sources/elbo-and-vae-lecture]] — Jensen's-inequality derivation, posterior-gap identity, reconstruction–regularisation decomposition, and EM/VAE optimisation paths.

## Up next

- [[ml_concepts/reparameterization-trick]] — how $\nabla_\phi \mathrm{ELBO}$ is computed in models where $q$ depends on a neural network.
- [[methods/vae]] — the canonical method built on the ELBO.
