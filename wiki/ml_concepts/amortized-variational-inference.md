---
title: Amortized Variational Inference
type: ml_concept
tags: [variational-inference, latent-variable-models, vae, neural-networks]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# Amortized Variational Inference

> Replace the per-example variational distribution $q(z)$ with a single network $q(z \mid x, \phi)$ that maps any $x$ to the parameters of its variational posterior. One model, one set of parameters $\phi$ — used for all examples.

## Motivation

We want to train a [[ml_concepts/latent-variable-model]] by maximising the [[ml_concepts/elbo|ELBO]] over both the generative parameters $\theta$ and an approximate posterior $q(z)$. Classical [[ml_concepts/variational-inference]] handles the $q$ side directly: for each observation $x$, fit a separate $q_x(z)$ from scratch. This is correct but unworkable at scale. Every new $x$ triggers a fresh optimisation, and storage of per-example variational parameters grows linearly with the dataset. At test time on unseen data the cost is even worse, because there is no precomputed $q$ to consult — you have to optimise again.

The workaround is to stop solving one inference problem per $x$ and instead learn one inference *function* that solves all of them. Pick a single network $q(z \mid x, \phi)$ with shared parameters $\phi$, where the input is $x$ and the output is the parameters of the variational distribution — typically the mean and variance of a diagonal Gaussian. Inference on any $x$, seen or unseen, collapses to one forward pass. The per-example $q$ has been replaced by a function $\phi$ that maps $x$ to $q(z \mid x)$.

This trade is not free. A function of finite capacity cannot match, for every $x$, the optimum that a hand-tuned per-example $q$ could reach. The shortfall is the **amortization gap**, separate from the family-induced [[ml_concepts/variational-inference|variational gap]]. The encoder is solving an average problem across the data distribution, not a tailored problem per example, and that averaging is the price of the speedup. In practice the gap is small relative to the cost saved, which is why amortised inference is the default in [[methods/vae|VAEs]] and related deep latent-variable models.

## Formal description

Pick a family parameterised by neural-net outputs. For a diagonal-Gaussian posterior, the encoder produces $(\mu_\phi(x), \sigma_\phi(x))$ and

$$
q(z \mid x, \phi) \;=\; \mathcal{N}\!\big(\mu_\phi(x),\,\mathrm{diag}(\sigma_\phi^2(x))\big).
$$

Training maximises the [[ml_concepts/elbo|ELBO]] jointly over the encoder parameters $\phi$ and the generative model parameters $\theta$:

$$
\max_{\theta, \phi}\;\mathbb{E}_{x \sim \pi}\!\big[\mathrm{ELBO}(\phi, \theta; x)\big] \;=\; \max_{\theta, \phi}\;\mathbb{E}_{x \sim \pi}\!\Big[\mathbb{E}_{z \sim q(z \mid x, \phi)}\big[\log p(x \mid z, \theta)\big] - \mathrm{KL}\!\big(q(z \mid x, \phi) \,\|\, p(z)\big)\Big].
$$

Backprop through $\mathbb{E}_{q}[\cdot]$ uses the [[ml_concepts/reparameterization-trick]]. The KL term is closed-form for Gaussian $q$ and Gaussian $p(z)$, so it does not need Monte Carlo.

## Why this is "amortization"

The term comes from cost accounting: instead of paying for a fresh optimisation per example, you pay once during training to learn $\phi$, then amortise that cost over all future examples. The lecture notes also call this **amortised inference network** or simply **encoder** (in the VAE context).

## Two failure modes

- **Amortization gap.** Even at the optimal $\phi$, $q(z \mid x, \phi)$ for a specific $x$ may be a worse approximation to the true posterior than a hand-fit $q$ would be. The encoder is solving an average problem, not a per-example problem.
- **Posterior collapse.** If the decoder $p(x \mid z, \theta)$ is too expressive (e.g. a strong autoregressive decoder), $q(z \mid x, \phi)$ collapses to the prior $p(z)$ — the KL term drops to zero, $z$ carries no information about $x$, and the latent code becomes useless. Standard mitigations: weaken the decoder, use KL annealing, or add information bottlenecks.

## Variations and related concepts

- [[ml_concepts/variational-inference]] — the parent framework.
- [[ml_concepts/elbo]] — the training objective.
- [[ml_concepts/reparameterization-trick]] — required for backprop through $\nabla_\phi$.
- [[methods/vae]] — the canonical amortised VI model.

## Open questions

- {none}

## Sources

- [[sources/elbo-and-vae-lecture]] — motivates the encoder as a way to replace per-example $q$ with a shared network mapping $x$ to posterior parameters.

## Up next

- [[ml_concepts/reparameterization-trick]] — how to backprop through $\nabla_\phi \mathbb{E}_{q(z \mid x, \phi)}[\cdot]$, the gradient amortisation creates.
- [[methods/vae]] — the canonical model that combines amortised inference with a generative decoder, trained end-to-end.
