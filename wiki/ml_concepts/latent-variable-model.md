---
title: Latent Variable Model
type: ml_concept
tags: [generative-models, latent-variable-models, variational-inference, vae]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# Latent Variable Model

> A generative model that draws each observation $x$ in two stages: first a latent $z \sim p(z)$ from a simple prior, then $x \sim p(x \mid z, \theta)$ from a learned conditional. Marginalising over $z$ turns a simple recipe into a flexible distribution.

## Motivation

We want a generative model for data $x$ — images, text, audio — whose marginal distribution is complex and high-dimensional. Directly parameterising $p(x \mid \theta)$ is a dead end: any expressive functional form for a density on a million-pixel space is intractable to normalise, and any tractable form (a Gaussian, a fully factorised model) is too rigid to fit real data.

The trick is to give up on a one-shot density and build it as a two-stage sampling process. Draw a latent $z$ from a simple prior $p(z)$ — typically $\mathcal{N}(0, I)$ — then draw $x$ from a parametric conditional $p(x \mid z, \theta)$, usually a neural network. Each $z$ becomes a low-dimensional summary (style, class, semantic content) and the network maps it to a distribution over observations. Sampling is now a forward pass: sample $z$ from the prior, then sample $x$ given $z$. The marginal $p(x \mid \theta) = \int p(x \mid z, \theta)\,p(z)\,dz$ can be arbitrarily complex even when both $p(z)$ and $p(x \mid z)$ are simple. This is the continuous version of the law of total probability: $P(A) = \sum_i P(A \mid B_i)\,P(B_i)$ writes a complex distribution as a mixture indexed by simple conditioning events, with $z$ playing the role of $B_i$.

The catch shows up the moment we try to train this model. Maximum likelihood needs $\log p(x \mid \theta)$, which requires the integral. There is no closed form, and the naive Monte Carlo estimator — average $p(x \mid z, \theta)$ over $z$ sampled from the prior — fails because the prior is uninformed about the specific $x$ we are conditioning on. Almost every prior sample lands on a $z$ that has nothing to do with $x$, so $p(x \mid z, \theta) \approx 0$ and the estimator has near-infinite variance.

This bottleneck is what motivates [[ml_concepts/variational-inference]] and the [[ml_concepts/elbo|ELBO]]. Instead of sampling $z$ blindly, sample from a distribution $q(z)$ biased toward latents that could plausibly have generated $x$. The price of that change of measure is a lower bound on the log-evidence rather than the log-evidence itself — a tractable surrogate that becomes the workhorse of training every modern latent-variable model.

## Formal description

A latent-variable generative model is specified by a prior and a likelihood:

$$
z \sim p(z), \qquad x \mid z \sim p(x \mid z, \theta).
$$

The marginal over observations is

$$
p(x \mid \theta) \;=\; \int p(x \mid z, \theta)\,p(z)\,dz.
$$

Training maximises $\sum_i \log p(x_i \mid \theta)$ over data, equivalently minimising the forward KL $\mathrm{KL}(\pi(x) \,\|\, p(x \mid \theta))$ between the data distribution $\pi$ and the model.

## Why naïve Monte Carlo fails

The marginal can be written as a prior expectation, $p(x \mid \theta) = \mathbb{E}_{z \sim p(z)}[p(x \mid z, \theta)]$, suggesting a direct estimator:

$$
p(x \mid \theta) \;\approx\; \frac{1}{K} \sum_{k=1}^K p(x \mid z_k, \theta), \qquad z_k \overset{\text{iid}}{\sim} p(z).
$$

This is hopeless when $p(x \mid z, \theta)$ is sharply peaked in $z$. For any specific $x$, only the few $z$ that explain it contribute meaningfully; everything else is essentially zero. Concrete failure: with $z \sim \mathcal{N}(0, 1)$ and $x \mid z \sim \mathcal{N}(z, \sigma^2)$ for small $\sigma$, the observation $x = 10$ is well-explained only by $z \approx 10$, but $z \sim \mathcal{N}(0, 1)$ essentially never produces such a sample. Required $K$ grows exponentially with the mismatch between prior and posterior.

This is the bottleneck that motivates [[ml_concepts/variational-inference]]: instead of sampling $z$ blindly from the prior, sample from a distribution $q(z)$ that concentrates on values explaining $x$. The price of the change of measure is the [[ml_concepts/elbo|ELBO]] bound on the log-evidence.

## Variations and related concepts

- [[ml_concepts/elbo]] — the bound that makes optimisation tractable.
- [[ml_concepts/variational-inference]] — the framework around approximate posteriors.
- [[ml_concepts/amortized-variational-inference]] — share one network across all $x$.
- [[methods/vae]] — the canonical latent-variable model with amortised inference.
- [[methods/variational-em]] — alternating optimisation of the model and the posterior.

## Open questions

- {none}

## Sources

- [[sources/elbo-and-vae-lecture]] — setup, motivation, and the naïve Monte Carlo failure mode.

## Up next

- [[ml_concepts/variational-inference]] — the framework that turns intractable posterior inference into tractable optimisation.
- [[ml_concepts/elbo]] — the lower bound on $\log p(x \mid \theta)$ that makes maximum-likelihood training of latent-variable models work.
