---
title: Variational EM
type: method
tags: [variational-inference, em-algorithm, latent-variable-models, optimisation]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# Variational EM

> Maximise the [[ml_concepts/elbo|ELBO]] by alternating: at fixed model parameters $\theta$, update the variational distribution $q$ to the closest tractable approximation of the true posterior (E-step); at fixed $q$, update $\theta$ to maximise the expected complete-data log-likelihood (M-step). Generalises the classical EM algorithm when the exact posterior $p(z \mid x, \theta)$ is intractable.

## Motivation

We want to fit a [[ml_concepts/latent-variable-model]] by maximum likelihood: $\max_\theta \log p(x \mid \theta) = \max_\theta \log \int p(x \mid z, \theta) p(z)\, dz$. Classical EM handles this when the posterior $p(z \mid x, \theta)$ has a closed form: the E-step computes the posterior exactly, the M-step maximises the expected complete-data log-likelihood under it, and the two together guarantee monotone non-decrease of $\log p(x \mid \theta)$. This works for Gaussian mixtures and HMMs.

For richer models — deep generative models, complex graphical structures — the exact posterior is intractable. The E-step breaks: there is no closed form to plug in, and Monte Carlo from the prior fails for the same reason the marginal does (almost no prior sample explains the data). Without a usable E-step, the monotonicity argument collapses and the algorithm has nothing to alternate.

Variational EM repairs the E-step by restricting $q$ to a tractable family $\mathcal{Q}$. The [[ml_concepts/elbo|ELBO]] identity $\log p(x \mid \theta) = \mathrm{ELBO}(q, \theta) + \mathrm{KL}(q \,\|\, p(z \mid x, \theta))$ says maximising the bound in $q$ is equivalent to minimising the KL to the true posterior — so the E-step becomes "project the posterior onto $\mathcal{Q}$", which is a tractable optimisation problem. The M-step is unchanged. Monotonicity is preserved for the bound, even though the bound's gap to $\log p$ no longer closes. This buys tractability at the cost of a fixed approximation gap, and trades the original "maximise $\log p$" guarantee for "maximise the ELBO". Whether that bound is tight enough is a question of the family $\mathcal{Q}$.

## Problem setting

We have a [[ml_concepts/latent-variable-model]] $p(x \mid \theta) = \int p(x \mid z, \theta) p(z)\,dz$ and want to maximise $\sum_i \log p(x_i \mid \theta)$. The integral is intractable, so we maximise its lower bound $\mathrm{ELBO}(q, \theta)$ jointly in $q$ (a variational distribution) and $\theta$.

## Algorithm

1. **Initialise** $\theta^{(0)}$.

2. **E-step.** At current $\theta^{(t)}$, update the variational distribution:

   $$
   q^{(t+1)} \;=\; \arg\max_{q}\,\mathrm{ELBO}(q, \theta^{(t)}).
   $$

   Because $\log p(x \mid \theta)$ does not depend on $q$, and $\log p(x \mid \theta) = \mathrm{ELBO}(q, \theta) + \mathrm{KL}(q \,\|\, p(z \mid x, \theta))$, maximising ELBO over $q$ is equivalent to minimising the KL to the true posterior:

   $$
   q^{(t+1)} \;=\; \arg\min_{q}\,\mathrm{KL}\!\big(q(z) \,\|\, p(z \mid x, \theta^{(t)})\big).
   $$

   If $q$ ranges over all distributions, the unique minimiser is the true posterior $p(z \mid x, \theta^{(t)})$ — this is the classical EM E-step. If $q$ is restricted to a tractable family $\mathcal{Q}$ (mean-field, parametric, etc.), the minimiser is the projection of the posterior onto $\mathcal{Q}$.

3. **M-step.** At fixed $q^{(t+1)}$, update the model parameters:

   $$
   \theta^{(t+1)} \;=\; \arg\max_{\theta}\,\mathrm{ELBO}(q^{(t+1)}, \theta).
   $$

   Dropping terms that don't depend on $\theta$:

   $$
   \theta^{(t+1)} \;=\; \arg\max_{\theta}\,\mathbb{E}_{z \sim q^{(t+1)}(z)}\!\big[\log p(x, z \mid \theta)\big].
   $$

   This is the expected complete-data log-likelihood under the current $q$.

4. **Repeat** until convergence.

## Why it works

Each iteration is guaranteed to not decrease $\log p(x \mid \theta)$:

- **E-step** moves $q$ to maximise the bound, so $\mathrm{ELBO}(q^{(t+1)}, \theta^{(t)}) \ge \mathrm{ELBO}(q^{(t)}, \theta^{(t)})$.
- **M-step** moves $\theta$ to maximise the (now-fixed) bound, so $\mathrm{ELBO}(q^{(t+1)}, \theta^{(t+1)}) \ge \mathrm{ELBO}(q^{(t+1)}, \theta^{(t)})$.

Combined: the bound is monotone non-decreasing. Because $\log p(x \mid \theta) \ge \mathrm{ELBO}(q, \theta)$ always, and the gap $\mathrm{KL}(q \,\|\, p(z \mid x, \theta))$ is closed at every E-step in the exact case, $\log p(x \mid \theta)$ itself does not decrease — this is the standard EM monotonicity argument.

In the approximate case (restricted $\mathcal{Q}$), the bound is monotone but the gap does not close, so the algorithm converges to a fixed point of the bound, not necessarily a maximum of $\log p$.

## Why VAEs don't do this verbatim

The E-step requires either the exact posterior $p(z \mid x, \theta^{(t)})$ — usually intractable — or finding the optimum in some family $\mathcal{Q}$. VAEs avoid both:

- The posterior is approximated by an [[ml_concepts/amortized-variational-inference|amortised]] encoder $q(z \mid x, \phi)$.
- Instead of fully optimising $\phi$ at each step, $\phi$ and $\theta$ are updated by joint SGD on the same loss.

The result is called **stochastic/generalised variational EM**: each "E-step" is a few SGD steps on $\phi$, each "M-step" a few SGD steps on $\theta$, in practice interleaved or fused into a single joint update. See [[methods/vae]] for the joint-update form.

## Comparison: classical EM vs Variational EM

| Aspect              | Classical EM                                                  | Variational EM                                                                 |
|---------------------|---------------------------------------------------------------|--------------------------------------------------------------------------------|
| E-step              | Compute $p(z \mid x, \theta^{(t)})$ exactly                   | Approximate it within $\mathcal{Q}$ by minimising KL                           |
| Tractability        | Requires closed-form posterior (e.g. GMM, HMM)                | Works with intractable posteriors                                              |
| Monotonicity in $\log p$ | Guaranteed                                                | Guaranteed for the ELBO; for $\log p$ only when E-step is exact                |
| Examples            | Gaussian mixtures, HMMs, mixture models                       | VAEs, deep latent variable models, mean-field VI                               |

## Properties

- **Convergence:** to a local maximum of the ELBO (not necessarily $\log p$). Initialisation matters.
- **Cost per iteration:** dominated by the E-step (posterior approximation) when the M-step has a closed form.
- **Failure modes:** the same restricted-family $q$ that makes the algorithm tractable also caps the achievable likelihood — a tight posterior approximation is a hard requirement.

## Variants and successors

- **Classical EM** — when the exact posterior is tractable.
- **VAE** ([[methods/vae]]) — amortised, joint SGD instead of strict alternation.
- **Wake-sleep algorithm** — Helmholtz machines, an earlier amortised-inference scheme that updates encoder and decoder in two separate phases.
- **VBEM / Mean-field VI** — variational Bayes EM with mean-field $q$, often closed-form coordinate ascent.

## Sources

- [[sources/elbo-and-vae-lecture]] — derivation of the E-step / M-step from ELBO, the equivalence "max ELBO in $q$ ≡ min KL to posterior", and the reasons VAE training departs from strict alternation.

## Up next

- [[methods/vae]] — replaces strict alternation with amortised joint SGD; the modern instantiation when $q$ is itself a neural network.
