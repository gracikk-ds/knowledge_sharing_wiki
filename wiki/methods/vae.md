---
title: Variational Autoencoder (VAE)
type: method
tags: [variational-inference, generative-models, latent-variable-models, vae, neural-networks]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# Variational Autoencoder (VAE)

> A deep latent-variable generative model trained by maximising the [[ml_concepts/elbo|ELBO]] with an [[ml_concepts/amortized-variational-inference|amortised]] Gaussian encoder and the [[ml_concepts/reparameterization-trick]] for end-to-end SGD. Encoder maps $x$ to the parameters of $q(z \mid x)$; decoder maps $z$ to a distribution over $x$.

## Motivation

The setup is a [[ml_concepts/latent-variable-model]] $p(x \mid \theta) = \int p(x \mid z, \theta)\, p(z)\, dz$ with a neural-network decoder. We want to train it by maximum likelihood on a large dataset of unlabeled $x$. The integral is intractable, so the training objective is the [[ml_concepts/elbo|ELBO]] instead, which needs an auxiliary distribution $q(z)$ over latents.

The [[methods/variational-em|variational EM]] view says: alternate. At fixed $\theta$, fit $q$ to the current posterior (E-step); at fixed $q$, update $\theta$ (M-step). Each E-step is itself an inner optimisation problem that has to be solved for *every* training example, then redone whenever $\theta$ moves. With deep decoders and millions of training points this is unworkable — the per-example posteriors do not have closed forms and there is no way to amortise the cost across examples or training steps.

The VAE replaces per-example optimisation with [[ml_concepts/amortized-variational-inference|amortisation]]: a single encoder network $q(z \mid x, \phi)$ predicts the parameters of $q$ as a function of $x$. Now the cost of inferring $q$ for a new example is one forward pass through the encoder, and the encoder's parameters $\phi$ are trained jointly with the decoder's $\theta$ on the same ELBO. The remaining technical issue is that $q$ depends on $\phi$ inside an expectation, so $\nabla_\phi \mathrm{ELBO}$ does not pass through the sampling step in the obvious way. The [[ml_concepts/reparameterization-trick]] solves it: write $z = \mu_\phi(x) + \sigma_\phi(x) \odot \varepsilon$ with $\varepsilon \sim \mathcal{N}(0, I)$, and gradients flow through $\mu_\phi, \sigma_\phi$ like any deterministic computation. With these two ingredients — amortised encoder, reparameterised sampling — the ELBO becomes a single differentiable loss that one optimiser can minimise end to end.

## Problem setting

Given iid data $\{x_i\}$ from an unknown $\pi(x)$, fit a [[ml_concepts/latent-variable-model]] $p(x \mid \theta) = \int p(x \mid z, \theta) p(z)\,dz$ so that

- new samples can be drawn from $p(x \mid \theta)$,
- $\log p(x \mid \theta)$ can be (approximately) evaluated on new data.

Maximum likelihood is intractable because the marginal integral has no closed form. VAEs sidestep this by maximising the ELBO with an amortised variational posterior.

## Architecture

Two networks share the same loss but have separate parameters:

- **Encoder $q(z \mid x, \phi)$**: input $x$, output the parameters of a diagonal Gaussian over $z$, $(\mu_\phi(x), \sigma_\phi(x))$. Implements [[ml_concepts/amortized-variational-inference]].
- **Decoder $p(x \mid z, \theta)$**: input $z$, output the parameters of a distribution over $x$ — typically a Gaussian (for continuous data, with mean predicted by the network) or a Bernoulli/categorical (for binary or discrete data).
- **Prior $p(z) = \mathcal{N}(0, I)$**: fixed standard normal.

The encoder–decoder split is the "autoencoder" structure; the "variational" part is that the bottleneck is stochastic and trained with a probabilistic loss.

## Algorithm

For each minibatch $\{x_i\}$:

1. **Encode**: compute $\mu_\phi(x_i), \sigma_\phi(x_i)$ for each $x_i$.
2. **Sample latent via reparameterization**: $\varepsilon^{(l)} \sim \mathcal{N}(0, I)$; $z_i^{(l)} = \mu_\phi(x_i) + \sigma_\phi(x_i) \odot \varepsilon^{(l)}$.
3. **Decode**: compute $\log p(x_i \mid z_i^{(l)}, \theta)$.
4. **Compute loss** = negative ELBO:

$$
\mathcal{L}_{\text{VAE}}(\phi, \theta; x_i) \;=\; -\frac{1}{L}\sum_{l=1}^L \log p\big(x_i \,\big|\, \mu_\phi(x_i) + \sigma_\phi(x_i) \odot \varepsilon^{(l)},\, \theta\big) \;+\; \frac{1}{2}\sum_{j=1}^d \!\Big(\mu_{\phi,j}^2(x_i) + \sigma_{\phi,j}^2(x_i) - \log \sigma_{\phi,j}^2(x_i) - 1\Big).
$$

5. **Backprop** through both networks and both terms jointly. Update $(\phi, \theta)$ by SGD.

In practice $L = 1$ is standard; larger $L$ reduces variance at proportional compute cost.

## Why the loss has that form

Start from the ELBO decomposition:

$$
\mathrm{ELBO}(\phi, \theta; x) \;=\; \mathbb{E}_{z \sim q(z \mid x, \phi)}\!\big[\log p(x \mid z, \theta)\big] - \mathrm{KL}\!\big(q(z \mid x, \phi) \,\|\, p(z)\big).
$$

- **Reconstruction term** $\mathbb{E}_q[\log p(x \mid z, \theta)]$: estimated by Monte Carlo with reparameterized samples. With Gaussian decoder, $\log p$ reduces to $-\tfrac{1}{2\sigma^2}\|x - \mu_\theta(z)\|^2 + \text{const}$ — an MSE up to constants. With Bernoulli decoder, binary cross-entropy.
- **KL term** $\mathrm{KL}(q(z \mid x, \phi) \,\|\, p(z))$: closed-form for Gaussian-vs-Gaussian, no Monte Carlo needed. See [[math_concepts/kl-divergence]]:

$$
\mathrm{KL}\!\big(\mathcal{N}(\mu_\phi(x), \mathrm{diag}(\sigma_\phi^2(x))) \,\|\, \mathcal{N}(0, I)\big) \;=\; \tfrac{1}{2}\sum_j \big(\mu_{\phi,j}^2(x) + \sigma_{\phi,j}^2(x) - \log \sigma_{\phi,j}^2(x) - 1\big).
$$

The KL gradient w.r.t. $\phi$ is exact (no sampling). The reconstruction gradient w.r.t. $\phi$ uses the reparameterization trick to pass through the sampling step.

## Why one optimiser, not EM

The [[methods/variational-em|variational EM]] view says: at fixed $\theta$, set $q$ to maximise ELBO (E-step); at fixed $q$, update $\theta$ (M-step). VAEs do both at once because:

1. The "exact E-step" $q = p(z \mid x, \theta)$ is intractable — $q$ is parameterised by a neural network, so we only approximate the maximum.
2. Both the reconstruction term and the KL term are already differentiable in $(\phi, \theta)$ inside one computation graph. There is no technical reason to separate the updates.

So in practice the loss is computed once and backpropagated through both networks simultaneously, exactly like training any deterministic deep net.

## Properties

- **Compute:** one forward pass through encoder, one sample $z$, one forward pass through decoder. Two backward passes (decoder, encoder).
- **Hyperparameters:** latent dimension $d$; decoder noise model (Gaussian vs Bernoulli); KL weight $\beta$ in the $\beta$-VAE variant.
- **Failure modes:**
  - **Posterior collapse** — encoder maps everything to the prior; latent code carries no information. Mitigations: weaker decoder, KL annealing, free bits.
  - **Blurry samples** — Gaussian decoder with fixed variance produces blurry $x$. Mitigations: per-pixel variance, hierarchical decoders, replace the Gaussian decoder with a flow or autoregressive model.
  - **Amortization gap** — encoder under-fits the optimal per-example posterior. Mitigations: more expressive encoder, iterative refinement at inference.

## Variants and successors

- **$\beta$-VAE** — multiply the KL term by $\beta > 1$ for disentangled latents (Higgins et al., 2017).
- **Conditional VAE (CVAE)** — condition encoder and decoder on a side input $c$ to model $p(x \mid c)$.
- **IWAE** — tighter importance-weighted bound replacing the single-sample ELBO (Burda et al., 2016).
- **VQ-VAE** — discrete latents trained with vector quantisation and straight-through estimator.
- **Hierarchical VAEs (e.g. NVAE)** — multi-level latent codes that fix posterior collapse with weak decoders.

## Sources

- [[sources/elbo-and-vae-lecture]] — derivation of the loss, the role of reparameterization, the closed-form Gaussian KL, and the argument for joint optimisation rather than alternating EM.

## Up next

- [[topics/variational-inference]] — the broader area: ELBO, amortised inference, reparameterisation, and how VAEs fit into it.
