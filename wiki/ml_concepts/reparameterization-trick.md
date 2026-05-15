---
title: Reparameterization Trick
type: ml_concept
tags: [variational-inference, vae, gradient-estimation, stochastic-computation]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# Reparameterization Trick

> Rewrite a sample $z \sim q(z \mid x, \phi)$ as a deterministic transform $z = g_\phi(x, \varepsilon)$ of noise $\varepsilon \sim p(\varepsilon)$ from a fixed distribution. The parameters $\phi$ now live inside $g_\phi$, not inside the sampling distribution, so $\nabla_\phi \mathbb{E}_q[f(z)]$ becomes a low-variance pathwise gradient.

## Motivation

To train [[ml_concepts/amortized-variational-inference]] we need the gradient

$$
\nabla_\phi\,\mathbb{E}_{z \sim q(z \mid x, \phi)}\big[f(z)\big],
$$

where $f(z) = \log p(x \mid z, \theta)$ is the reconstruction term in the [[ml_concepts/elbo|ELBO]]. The obstacle is structural: the distribution we sample from depends on the parameters we want to differentiate. The expectation and the gradient cannot be swapped freely, because changing $\phi$ changes *which $z$ get sampled*, not just what value $f$ takes on them.

The naive approach — sample $z \sim q(z \mid x, \phi)$, compute $\nabla_\phi f(z)$, and call it a gradient estimate — is plainly wrong. The drawn $z$ depends on $\phi$ through the sampler, which is a non-differentiable operation. Backprop through `sample()` is not defined.

There is a general unbiased estimator that works for any $q$, called the **score-function (REINFORCE) estimator**:

$$
\nabla_\phi\,\mathbb{E}_{q(z \mid x, \phi)}[f(z)] \;=\; \mathbb{E}_{q}\!\big[f(z) \cdot \nabla_\phi \log q(z \mid x, \phi)\big].
$$

It is correct, but it treats $f(z)$ as a black-box scalar multiplier on a noisy score, ignoring the structure of $f$. Variance is high enough to make training of continuous latents slow or unstable.

The reparameterization trick fixes the source of the problem rather than working around it. Rewrite $z$ as a deterministic transform of *fixed* noise: $z = g_\phi(x, \varepsilon)$ with $\varepsilon \sim p(\varepsilon)$ independent of $\phi$. Now the distribution we sample from no longer depends on $\phi$; only the deterministic function $g_\phi$ does. Gradients become an ordinary chain rule through $g_\phi$, the whole graph is differentiable end-to-end, and a single sample of $\varepsilon$ gives a low-variance pathwise gradient that passes information through $f$ rather than averaging it out. This is why [[methods/vae|VAEs]] use it as the default and reserve the score-function estimator for cases where reparameterization is not available (discrete latents, mixtures).

## Formal description

Suppose $z \sim q(z \mid x, \phi)$ admits the representation $z = g_\phi(x, \varepsilon)$ with $\varepsilon \sim p(\varepsilon)$ independent of $\phi$. By the law of the unconscious statistician (LOTUS),

$$
\mathbb{E}_{z \sim q(z \mid x, \phi)}\big[f(z)\big] \;=\; \mathbb{E}_{\varepsilon \sim p(\varepsilon)}\big[f(g_\phi(x, \varepsilon))\big].
$$

The right-hand side has no parameter-dependent measure, so under standard regularity conditions:

$$
\nabla_\phi\,\mathbb{E}_{z \sim q}[f(z)] \;=\; \mathbb{E}_{\varepsilon \sim p(\varepsilon)}\!\big[\nabla_\phi f(g_\phi(x, \varepsilon))\big].
$$

By the chain rule on the integrand:

$$
\nabla_\phi f(g_\phi(x, \varepsilon)) \;=\; \big(\nabla_z f(z)\big)\big|_{z = g_\phi(x, \varepsilon)} \cdot \nabla_\phi g_\phi(x, \varepsilon).
$$

Monte Carlo with $L$ samples (often $L = 1$ per example):

$$
\nabla_\phi\,\mathbb{E}_{z \sim q}[f(z)] \;\approx\; \frac{1}{L}\sum_{l=1}^L \nabla_\phi f(g_\phi(x, \varepsilon^{(l)})), \qquad \varepsilon^{(l)} \sim p(\varepsilon).
$$

## Canonical instance: diagonal Gaussian

For a diagonal-Gaussian posterior $q(z \mid x, \phi) = \mathcal{N}(\mu_\phi(x), \mathrm{diag}(\sigma_\phi^2(x)))$, choose $p(\varepsilon) = \mathcal{N}(0, I)$ and

$$
z \;=\; g_\phi(x, \varepsilon) \;=\; \mu_\phi(x) + \sigma_\phi(x) \odot \varepsilon.
$$

The encoder outputs $\mu_\phi$ and $\sigma_\phi$ (or $\log \sigma_\phi$); both are differentiable functions of $\phi$. The randomness comes from $\varepsilon$ and contributes no gradient.

For more general distributions there are alternatives: location-scale families have a straightforward reparameterization; mixture and discrete distributions need different tools (Gumbel-softmax, straight-through estimators, etc.).

## Contrast with the score-function estimator

The general identity for differentiating an expectation with parameter-dependent measure is the **score-function (REINFORCE) estimator**:

$$
\nabla_\phi\,\mathbb{E}_{q(z \mid x, \phi)}[f(z)] \;=\; \mathbb{E}_{q}\!\big[f(z) \cdot \nabla_\phi \log q(z \mid x, \phi)\big].
$$

It is unbiased for *any* $q$, including discrete ones, but treats $f(z)$ as a black-box scalar multiplier on a noisy score. Variance is typically much higher than reparameterization, because reparameterization passes gradient information through the structure of $f$ via the chain rule rather than as a scalar coefficient.

In VAEs reparameterization is the default, with score-function reserved for discrete latents or distributions where reparameterization isn't possible.

## Variations and related concepts

- [[ml_concepts/elbo]] — the loss whose $\phi$-gradient needs this trick.
- [[ml_concepts/amortized-variational-inference]] — the setting where $\phi$ are encoder weights.
- [[methods/vae]] — the canonical use of the reparameterization trick.
- [[ml_concepts/variational-inference]] — the framework around all of this.

## Open questions

- {none}

## Sources

- [[sources/elbo-and-vae-lecture]] — derivation via LOTUS and contrast with the score-function estimator.

## Up next

- [[methods/vae]] — the canonical model where the reparameterization trick lets the encoder, decoder, and ELBO be trained jointly by SGD.
