---
title: "ELBO and VAE — lecture"
type: source
source_path: raw/lectures/ELBO_and_VAE.md
source_kind: lecture
source_date: 2025-10-26
ingested: 2026-05-15
tags: [variational-inference, latent-variable-models, elbo, vae, reparameterization, kl-divergence]
sources: 1
status: draft
---

# ELBO and VAE — lecture

> A self-contained lecture deriving ELBO from first principles, decomposing it into reconstruction and regularisation, and walking through the full VAE training story including the reparameterization trick and the closed-form Gaussian KL.

## Key takeaways

- **Why MLE alone is not enough.** Forward KL minimisation $\mathrm{KL}(\pi \,\|\, p_\theta)$ reduces to maximising $\mathbb{E}_\pi[\log p(x \mid \theta)]$. Even if we learn $p(x \mid \theta)$ as a parametric density, sampling from it can remain hard — motivating the latent-variable structure.
- **Latent-variable models** factor $p(x \mid \theta) = \int p(x \mid z, \theta) p(z) dz$. Sampling becomes trivial; the marginal can be arbitrarily complex even from simple components.
- **Naïve Monte Carlo over the prior fails.** For any specific $x$, only the few $z$ that explain it matter; prior samples are nearly all irrelevant. Required sample count grows with the prior–posterior mismatch.
- **ELBO via Jensen.** Insert $q(z)/q(z)$, apply Jensen on concave $\log$: $\log p(x \mid \theta) \ge \mathbb{E}_q[\log p(x, z \mid \theta)/q(z)]$. The bound holds for any valid $q$.
- **ELBO via Bayes.** Using $p(x, z) = p(z \mid x) p(x)$ gives the exact identity $\log p(x \mid \theta) = \mathrm{ELBO}(q, \theta) + \mathrm{KL}(q(z) \,\|\, p(z \mid x, \theta))$. The gap is exactly the KL from $q$ to the true posterior; equality iff $q = p(z \mid x, \theta)$.
- **Decomposition into reconstruction + regularisation.** Splitting $p(x, z) = p(x \mid z) p(z)$ gives $\mathrm{ELBO} = \mathbb{E}_q[\log p(x \mid z, \theta)] - \mathrm{KL}(q(z) \,\|\, p(z))$ — the VAE loss.
- **Variational EM.** Alternate: E-step at fixed $\theta$ maximises ELBO over $q$ (equivalent to minimising KL to the posterior); M-step at fixed $q$ maximises ELBO over $\theta$.
- **Amortised inference.** Replace per-example $q$ with a network $q(z \mid x, \phi)$ to handle two problems at once: intractability of the exact posterior, and the need for a different $q$ per $x$.
- **Reparameterization trick.** Rewrite $z \sim q(z \mid x, \phi)$ as $z = g_\phi(x, \varepsilon)$ with $\varepsilon \sim p(\varepsilon)$ fixed. By LOTUS the expectation is now over a $\phi$-independent measure; gradients flow through $g_\phi$. The score-function alternative is unbiased but high-variance.
- **Final VAE loss.** With Gaussian encoder and $\mathcal{N}(0, I)$ prior, the KL is closed-form (sum of $\mu_j^2 + \sigma_j^2 - \log\sigma_j^2 - 1$ over latent dims). Reconstruction term uses one reparameterized sample; whole loss is one SGD step on $(\phi, \theta)$.

## Concepts touched

- [[ml_concepts/elbo]] — central concept of the lecture; derived two ways (Jensen and Bayes), decomposed three ways (raw, with posterior gap, reconstruction+regularisation). New page.
- [[ml_concepts/latent-variable-model]] — the setup; analogy with the law of total probability; naïve Monte Carlo failure mode. New page.
- [[ml_concepts/variational-inference]] — framework; the identity that lets us optimise ELBO without ever computing the true KL. New page.
- [[ml_concepts/amortized-variational-inference]] — encoder as a network mapping $x$ to posterior parameters; motivated by intractability and the "different $q$ per $x$" problem. New page.
- [[ml_concepts/reparameterization-trick]] — LOTUS-based derivation; canonical Gaussian instance; contrast with score-function estimator. New page.
- [[math_concepts/kl-divergence]] — defining the bound's gap; closed-form Gaussian KL used in the VAE loss; non-negativity proof. New page.
- [[math_concepts/jensens-inequality]] — used to turn $\log \mathbb{E}_q[\cdot]$ into $\mathbb{E}_q[\log \cdot]$. New page.
- [[methods/vae]] — algorithm, architecture, why one joint optimiser instead of EM. New page.
- [[methods/variational-em]] — alternation framework, equivalence "max ELBO in $q$ ≡ min KL to posterior", why VAE doesn't do strict EM. New page.

## Contradictions and revisions

None. This is the first ingest in the variational-inference region of the wiki; nothing existing to contradict.

## Questions raised

None surfaced yet. Possible follow-ups for later sources: the amortization gap (quantitative effect), posterior collapse (why some decoders trigger it), tighter bounds (IWAE), and the role of forward vs reverse KL in different generative-modelling paradigms.

## Notes

- The lecture uses Russian-language prose with English-language formulas. Concepts and notation are standard.
- It cross-references its own sub-sections via Notion-style links; these refer to internal structure of the source and do not require wiki pages.
- The naïve Monte Carlo example ($x = 10$, $z \sim \mathcal{N}(0, 1)$, $\sigma = 0.1$) is a concrete illustration of prior–posterior mismatch — captured on [[ml_concepts/latent-variable-model]] in the "Why naïve Monte Carlo fails" section.
- The score-function estimator is mentioned only as a high-variance alternative to reparameterization and not derived; covered briefly on [[ml_concepts/reparameterization-trick]]. A dedicated source could expand it into its own page.

## Pointer back to raw

`raw/lectures/ELBO_and_VAE.md`
