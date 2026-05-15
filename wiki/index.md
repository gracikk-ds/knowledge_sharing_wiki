---
title: Wiki Index
type: index
created: 2026-05-15
updated: 2026-05-15
---

# Wiki Index

_Last updated: 2026-05-15_

## Start here

Topic primers are the entry points for sequential study — each walks through an area in motivated build-up voice with inline links into the reference layer.

- [[topics/variational-inference]] — latent-variable generative modelling trained by approximating the intractable posterior and maximising the ELBO. Path: latent-variable-model → variational-inference → ELBO → variational-em → amortized-vi → reparameterization → VAE.
- [[topics/few-step-generative-models]] — turning slow many-step ODE generators (diffusion, flow matching) into 1–4-step samplers via flow maps and step distillation. Path: probability-flow-ODE → flow-map → consistency-function → step-distillation → progressive-distillation → CMs → multistep-CMs → shortcut → mean-flow.

The catalog below is alphabetical by type, optimised for refresh and lookup.

## ML concepts

- [[ml_concepts/amortized-variational-inference]] — replace per-example $q(z)$ with a single network $q(z \mid x, \phi)$ shared across all examples.
- [[ml_concepts/consistency-function]] — a learned $(x_t, t) \mapsto x_0$ map that is constant along each probability-flow ODE trajectory.
- [[ml_concepts/diffusion-model]] — generative model defined by a forward noising process and a learned reverse process (stub).
- [[ml_concepts/elbo]] — tractable lower bound on $\log p(x \mid \theta)$, central training objective of variational inference and VAEs.
- [[ml_concepts/flow-map]] — the integrated solution of a generative ODE, learnt directly instead of its derivative.
- [[ml_concepts/flow-matching]] — framework that learns a velocity field of an ODE transporting prior to data (stub).
- [[ml_concepts/latent-variable-model]] — generative model that samples $z \sim p(z)$ then $x \sim p(x \mid z, \theta)$; marginalising builds complex distributions from simple parts.
- [[ml_concepts/probability-flow-ode]] — deterministic ODE whose marginals match those of a diffusion SDE (stub).
- [[ml_concepts/reparameterization-trick]] — rewrite $z \sim q(z \mid x, \phi)$ as $z = g_\phi(x, \varepsilon)$ so gradients flow through a deterministic transform.
- [[ml_concepts/score-function]] — gradient of the log-density of the noised marginal, used by score-based models (stub).
- [[ml_concepts/step-distillation]] — train a fast student to mimic a slow multi-step teacher's deterministic ODE output.
- [[ml_concepts/variational-inference]] — approximate an intractable posterior by the closest distribution in a tractable family under reverse KL.

## Math concepts

- [[math_concepts/jensens-inequality]] — for convex $\varphi$, $\varphi(\mathbb{E}[X]) \le \mathbb{E}[\varphi(X)]$; concave flips the sign.
- [[math_concepts/kl-divergence]] — non-negative asymmetric measure $\mathrm{KL}(q \,\|\, p) = \mathbb{E}_q[\log q/p]$ of how much $q$ differs from $p$.
- [[math_concepts/mean-flow-identity]] — $F(x_t, t, s) = v(x_t, t) - (s - t)\,\mathrm{d}F/\mathrm{d}t$ relating average velocity to instantaneous velocity.

## Methods

- [[methods/consistency-distillation]] — train a consistency function using one teacher solver step per pair.
- [[methods/consistency-training]] — train a consistency function without a teacher via a same-$\epsilon$ straight-path pair.
- [[methods/mean-flow]] — flow map trained to match the average velocity over $[t, s]$ via the Mean Flow Identity.
- [[methods/multistep-consistency-model]] — split $[0, \sigma]$ into intervals and learn one consistency function per interval.
- [[methods/progressive-distillation]] — iteratively halve sampling steps by distilling 2-step teacher behaviour into 1-step student (stub).
- [[methods/shortcut-model]] — flow map trained with a stop-gradient interval-additivity self-consistency loss.
- [[methods/vae]] — latent-variable generative model trained by maximising ELBO with a Gaussian amortised encoder and the reparameterization trick.
- [[methods/variational-em]] — alternate E-step (update $q$ at fixed $\theta$) and M-step (update $\theta$ at fixed $q$) to maximise ELBO.

## Topics

- [[topics/few-step-generative-models]] — design space of generators that sample in 1–4 forward passes.
- [[topics/variational-inference]] — latent-variable generative modelling trained via ELBO maximisation and approximate posteriors.

## Sources

- [[sources/elbo-and-vae-lecture]] — lecture deriving ELBO and walking through the full VAE training story with reparameterization.
- [[sources/flow-map-models-lecture]] — lecture covering CMs, multistep CMs, ShortCut, and Mean Flow under the unifying flow-map view.

## Questions

- [[questions/how-is-mean-flow-time-derivative-computed]] — how is $\mathrm{d}F/\mathrm{d}t$ along the trajectory computed for the Mean Flow loss?
- [[questions/why-cant-cms-use-ode-solvers]] — why are CMs incompatible with standard ODE solvers?
- [[questions/why-does-consistency-training-work-without-teacher]] — why does the same-$\epsilon$ straight-path trick suffice without a teacher?
