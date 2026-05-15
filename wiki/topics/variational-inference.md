---
title: Variational Inference
type: topic
tags: [variational-inference, latent-variable-models, generative-models, elbo, vae]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# Variational Inference

> A family of generative models that train a latent-variable model by approximating its intractable posterior with a tractable distribution and maximising the [[ml_concepts/elbo|ELBO]] in place of the true log-likelihood.

## The setting

Latent-variable generative models posit that every data point $x$ is generated from an unobserved $z$: draw $z \sim p(z)$ from a simple prior, then $x \sim p(x \mid z, \theta)$ from a conditional. The thing you actually want — maximum likelihood — needs the marginal $p(x \mid \theta) = \int p(x \mid z, \theta) p(z) dz$, integrated over all possible latents.

That integral is intractable in general. There is no closed form for any model interesting enough to be worth fitting, and the naive Monte Carlo workaround — sample $z \sim p(z)$ and average the conditional — fails. For any specific $x$, the latents that could plausibly explain it occupy a thin region of the prior, and almost every prior sample lands outside it. The integrand is near zero for those samples; your estimator is dominated by noise and the gradient is useless for training.

Variational inference attacks this with one move: introduce a second distribution $q(z)$ whose mass sits where the integrand is large, then bound $\log p(x \mid \theta)$ by a quantity you can estimate from $q$-samples. The bound is the ELBO. The rest of the area is the design space around that move — what shape $q$ takes, how you fit it, how you backprop through it.

## Core ideas

The starting point is the [[ml_concepts/latent-variable-model]] itself — a generative story where $x$ is observed, $z$ is not, and the two are joined by a prior $p(z)$ and a conditional $p(x \mid z, \theta)$. The marginal integral is where everything breaks. Everything below is workarounds.

The framework's central idea is [[ml_concepts/variational-inference]]: approximate the true posterior $p(z \mid x, \theta)$ with the closest distribution $q$ in some tractable family under reverse KL. The direction is "reverse" because the expectation is taken under $q$, which is what you can actually sample from. Reverse KL is mode-seeking — it puts $q$'s mass on the highest peaks of the posterior and ignores low-mass regions, which has consequences discussed on the page.

From this falls out the [[ml_concepts/elbo]]: a tractable lower bound on $\log p(x \mid \theta)$ that you can estimate from $q$-samples. The bound's slack is exactly $\mathrm{KL}(q \,\|\, p(z \mid x))$, so maximising the bound jointly in $q$ and $\theta$ also pushes $q$ toward the true posterior. Two pieces of math sit underneath: [[math_concepts/jensens-inequality]] gives the bound direction, and [[math_concepts/kl-divergence]] measures both the slack and the regulariser term that appears in the loss in practice.

Two ideas turn the framework into a trainable system. [[ml_concepts/amortized-variational-inference]] replaces a per-example $q$ with a single neural network $q(z \mid x, \phi)$ shared across all $x$ — cheaper at inference, mildly sub-optimal per example. And [[ml_concepts/reparameterization-trick]] rewrites a sample $z \sim q(z \mid x, \phi)$ as a deterministic transform $z = g_\phi(x, \varepsilon)$ of fixed-distribution noise $\varepsilon$, so the gradient $\nabla_\phi \mathbb{E}_q[\cdot]$ becomes an expectation over $\varepsilon$ and you can backprop through the sampling step.

## Methods that grow from these ideas

[[methods/variational-em]] is the textbook way. Alternate an E-step that updates $q$ at fixed $\theta$ with an M-step that updates $\theta$ at fixed $q$. It pre-dates deep learning by decades and works whenever $q$ has a tractable form and the E-step admits a closed-form solution. It is useful for understanding what the ELBO is *trying* to do at each step, but it scales poorly to high-dimensional models where the exact E-step is itself intractable.

The modern method is the [[methods/vae]]. The encoder (an amortised $q$) and the decoder (the $p(x \mid z, \theta)$) are both neural networks. The KL term becomes a closed-form Gaussian-vs-Gaussian expression; the reconstruction term is a Monte Carlo estimate using a single reparameterized sample; the gradient flows through both terms in one computation graph. The decision to drop the EM alternation — at fixed $\theta$ the exact E-step is intractable anyway, since $q$ is itself a neural network — is what makes the VAE work end-to-end.

## Open threads

- **Amortization gap.** Quantitatively, how much does the shared encoder under-fit the per-example optimum? Mentioned on [[ml_concepts/amortized-variational-inference]] but not analysed.
- **Posterior collapse.** Conditions under which $q(z \mid x, \phi) \to p(z)$ and the latent code becomes uninformative; mitigations.
- **Score-function estimator.** Used in discrete-latent and non-reparameterizable settings; only briefly mentioned on [[ml_concepts/reparameterization-trick]].
- **Tighter bounds.** Importance-weighted ELBO (IWAE); $\beta$-VAE and information-theoretic objectives.

## Reading order (recap)

1. [[ml_concepts/latent-variable-model]]
2. [[ml_concepts/variational-inference]]
3. [[ml_concepts/elbo]] — referring to [[math_concepts/jensens-inequality]] and [[math_concepts/kl-divergence]] as needed
4. [[methods/variational-em]]
5. [[ml_concepts/amortized-variational-inference]]
6. [[ml_concepts/reparameterization-trick]]
7. [[methods/vae]]

## Reading queue

- Kingma & Welling, "Auto-Encoding Variational Bayes" (2014) — original VAE paper.
- Rezende, Mohamed, Wierstra, "Stochastic Backpropagation and Approximate Inference in Deep Generative Models" (2014) — concurrent reparameterization-trick paper.
- Burda, Grosse, Salakhutdinov, "Importance Weighted Autoencoders" (IWAE, 2016) — tighter bound.
- Higgins et al., "$\beta$-VAE" (2017) — disentanglement via reweighted KL.
- Kingma & Welling, "An Introduction to Variational Autoencoders" (Foundations and Trends, 2019) — long-form survey.
