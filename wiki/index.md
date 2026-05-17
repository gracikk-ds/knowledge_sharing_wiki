---
title: Wiki Index
type: index
created: 2026-05-15
updated: 2026-05-17
---

# Wiki Index

_Last updated: 2026-05-17_

## Start here

Topic primers are the entry points for sequential study — each walks through an area in motivated build-up voice with inline links into the reference layer.

- [[topics/variational-inference]] — latent-variable generative modelling trained by approximating the intractable posterior and maximising the ELBO. Path: latent-variable-model → variational-inference → ELBO → variational-em → amortized-vi → reparameterization → VAE.
- [[topics/few-step-generative-models]] — turning slow many-step ODE generators (diffusion, flow matching) into 1–4-step samplers via flow maps and step distillation. Path: probability-flow-ODE → flow-map → consistency-function → step-distillation → progressive-distillation → CMs → multistep-CMs → shortcut → mean-flow.
- [[topics/positional-encoding]] — injecting position into self-attention. Path: self-attention → positional-encoding → rotation-matrix-2d → RoPE → sinusoidal/learned-absolute → RoPE method (1D/2D/3D) → PI → NTK-Aware → YaRN → DyPE.
- [[topics/transformers]] — encoder-decoder attention architecture (Vaswani 2017). Path: self-attention → positional-encoding → multi-head-attention → causal-masking → cross-attention → transformer (architecture) → BERT/GPT/T5/ViT (stubs).
- [[topics/attention-variants]] — modern attention zoo organised around the KV-cache bottleneck. Path: kv-cache → MHA → MQA → GQA → MLA → attention-sink → gated-attention → linear-attention (GLA, hybrids) → sliding-window → document-masking.

The catalog below is alphabetical by type, optimised for refresh and lookup.

## ML concepts

- [[ml_concepts/amortized-variational-inference]] — replace per-example $q(z)$ with a single network $q(z \mid x, \phi)$ shared across all examples.
- [[ml_concepts/attention-sink]] — phenomenon where a few "sink" positions accumulate disproportionate attention weight without semantic load; destabilises training (stub).
- [[ml_concepts/causal-masking]] — zero-out scores for future positions ($-\infty$ before softmax) so each position attends only to itself and the past; required for autoregressive decoders.
- [[ml_concepts/consistency-function]] — a learned $(x_t, t) \mapsto x_0$ map that is constant along each probability-flow ODE trajectory.
- [[ml_concepts/cross-attention]] — same mechanism as self-attention but $Q$ comes from one sequence and $K, V$ from another; the encoder-decoder bridge in seq2seq transformers.
- [[ml_concepts/diffusion-model]] — generative model defined by a forward noising process and a learned reverse process (stub).
- [[ml_concepts/document-masking]] — block-diagonal causal mask that prevents attention from crossing boundaries between packed documents; non-negotiable for 64k+ contexts.
- [[ml_concepts/elbo]] — tractable lower bound on $\log p(x \mid \theta)$, central training objective of variational inference and VAEs.
- [[ml_concepts/flow-map]] — the integrated solution of a generative ODE, learnt directly instead of its derivative.
- [[ml_concepts/flow-matching]] — framework that learns a velocity field of an ODE transporting prior to data (stub).
- [[ml_concepts/gated-attention]] — sigmoid gate $\sigma(W^G x_t)$ elementwise multiplied into the attention output to suppress attention sinks and stabilise training.
- [[ml_concepts/grouped-query-attention]] — heads split into $g$ groups, each group shares one $K, V$ pair; KV-cache reduced by $h/g$; with small groups outperforms MHA on ablations. Modern default.
- [[ml_concepts/kv-cache]] — inference-time table of stored $K, V$ per position per head; size $2 \cdot n_{\text{heads}} \cdot n_{\text{layers}} \cdot d_{\text{head}} \cdot L$. The bottleneck around which MQA/GQA/MLA exist.
- [[ml_concepts/latent-variable-model]] — generative model that samples $z \sim p(z)$ then $x \sim p(x \mid z, \theta)$; marginalising builds complex distributions from simple parts.
- [[ml_concepts/linear-attention]] — drop softmax, refactor $\sum_j (q_t^\top k_j) v_j$ as a recurrent state $S_t = \sum_j v_j k_j^\top$; $O(1)$ memory per step; GLA adds a forget gate; used in hybrid stacks.
- [[ml_concepts/multi-head-attention]] — $h$ parallel self-attention blocks with independent $W_Q^{(i)}, W_K^{(i)}, W_V^{(i)}$; concat + projection $W^O$; each head specialises on a different relation type.
- [[ml_concepts/multi-latent-attention]] — compress KV into a low-dim latent $c_t$, decompress to $K, V$ on the fly; 4–8× cache compression while keeping capacity. DeepSeek, Kimi-K2.
- [[ml_concepts/multi-query-attention]] — all heads share one $K, V$ pair; KV-cache divided by $n_{\text{heads}}$ at the cost of expressivity. Loses to MHA in ablations.
- [[ml_concepts/positional-encoding]] — mechanism for injecting token position into self-attention; key axis is additive vs multiplicative.
- [[ml_concepts/probability-flow-ode]] — deterministic ODE whose marginals match those of a diffusion SDE (stub).
- [[ml_concepts/reparameterization-trick]] — rewrite $z \sim q(z \mid x, \phi)$ as $z = g_\phi(x, \varepsilon)$ so gradients flow through a deterministic transform.
- [[ml_concepts/rotary-position-embedding]] — encode position by rotating $q, k$ at angles proportional to position so that $q_m^\top k_n$ depends only on content and $(n - m)$.
- [[ml_concepts/score-function]] — gradient of the log-density of the noised marginal, used by score-based models (stub).
- [[ml_concepts/self-attention]] — Q/K/V projections from each token's embedding; output is softmax-weighted sum of values over all positions, weights from scaled dot-product of Q and K.
- [[ml_concepts/sliding-window-attention]] — restrict each position to a window of $p$ previous tokens; $O(L \cdot p)$ instead of $O(L^2)$; usually interleaved with full attention.
- [[ml_concepts/step-distillation]] — train a fast student to mimic a slow multi-step teacher's deterministic ODE output.
- [[ml_concepts/variational-inference]] — approximate an intractable posterior by the closest distribution in a tractable family under reverse KL.

## Math concepts

- [[math_concepts/jensens-inequality]] — for convex $\varphi$, $\varphi(\mathbb{E}[X]) \le \mathbb{E}[\varphi(X)]$; concave flips the sign.
- [[math_concepts/kl-divergence]] — non-negative asymmetric measure $\mathrm{KL}(q \,\|\, p) = \mathbb{E}_q[\log q/p]$ of how much $q$ differs from $p$.
- [[math_concepts/mean-flow-identity]] — $F(x_t, t, s) = v(x_t, t) - (s - t)\,\mathrm{d}F/\mathrm{d}t$ relating average velocity to instantaneous velocity.
- [[math_concepts/rotation-matrix-2d]] — $R(\theta) \in \mathbb{R}^{2 \times 2}$; ortho, composition $R(\alpha)R(\beta)=R(\alpha+\beta)$, $R^\top=R^{-1}=R(-\theta)$.

## Methods

- [[methods/consistency-distillation]] — train a consistency function using one teacher solver step per pair.
- [[methods/consistency-training]] — train a consistency function without a teacher via a same-$\epsilon$ straight-path pair.
- [[methods/dype]] — dynamic RoPE extrapolation for diffusion: $\kappa(t)$-scaled PI/NTK/YaRN that fades to identity on late sampling steps.
- [[methods/learned-absolute-position-embedding]] — trainable $E \in \mathbb{R}^{L_{\max} \times d}$ added to token embedding; hard length cap.
- [[methods/mean-flow]] — flow map trained to match the average velocity over $[t, s]$ via the Mean Flow Identity.
- [[methods/multistep-consistency-model]] — split $[0, \sigma]$ into intervals and learn one consistency function per interval.
- [[methods/ntk-aware-interpolation]] — scale RoPE base $b \to b \cdot s^{d/(d-2)}$; non-uniform compression preserves fast pairs.
- [[methods/position-interpolation]] — scale RoPE positions $m \to m/s$ to fit angles back into the trained range; uniform compression.
- [[methods/progressive-distillation]] — iteratively halve sampling steps by distilling 2-step teacher behaviour into 1-step student (stub).
- [[methods/rope]] — block-diagonal $d/2$ 2D rotations with frequency schedule $\theta_i = 10000^{-2i/d}$; 1D, 2D (ViT), and 3D (video) variants.
- [[methods/shortcut-model]] — flow map trained with a stop-gradient interval-additivity self-consistency loss.
- [[methods/sinusoidal-position-encoding]] — fixed sine/cosine PE added to token embedding (Vaswani et al., 2017).
- [[methods/transformer]] — Vaswani 2017 encoder-decoder architecture: 6+6 stacks of (masked) self-attention + (cross-attention) + FFN, residual + LayerNorm, sinusoidal PE, final linear + softmax.
- [[methods/vae]] — latent-variable generative model trained by maximising ELBO with a Gaussian amortised encoder and the reparameterization trick.
- [[methods/variational-em]] — alternate E-step (update $q$ at fixed $\theta$) and M-step (update $\theta$ at fixed $q$) to maximise ELBO.
- [[methods/yarn]] — three-zone RoPE context extension by wavelength + softmax temperature correction.

## Topics

- [[topics/attention-variants]] — modern attention zoo organised around the KV-cache bottleneck: MHA → MQA → GQA → MLA spectrum, gated and linear attention, long-context masks (SWA, dual chunk, document masking).
- [[topics/few-step-generative-models]] — design space of generators that sample in 1–4 forward passes.
- [[topics/positional-encoding]] — how to inject token position into self-attention, from additive baselines to RoPE and its context-extension methods.
- [[topics/transformers]] — Vaswani 2017 architecture and its descendants (BERT/GPT/T5/ViT); core ideas of self-attention, multi-head, positional encoding, masking, cross-attention; $O(L^2)$ as the long-term bottleneck.
- [[topics/variational-inference]] — latent-variable generative modelling trained via ELBO maximisation and approximate posteriors.

## Sources

- [[sources/attention-mechanisms-lecture]] — lecture surveying modern attention variants organised around the KV-cache: MHA/MQA/GQA/MLA spectrum, gated and linear (GLA) attention, long-context patterns (SWA, dual chunk, doc masking) with concrete frontier models.
- [[sources/elbo-and-vae-lecture]] — lecture deriving ELBO and walking through the full VAE training story with reparameterization.
- [[sources/flow-map-models-lecture]] — lecture covering CMs, multistep CMs, ShortCut, and Mean Flow under the unifying flow-map view.
- [[sources/illustrated-transformer]] — visual walk-through of Vaswani 2017 architecture: encoder/decoder stacks, self-attention step by step, multi-head, sinusoidal PE, residual+LayerNorm, masked + cross-attention, final linear+softmax.
- [[sources/rope-lecture]] — 5-part lecture: PE motivation, RoPE 2D intuition, $d$-dim algorithm, 2D/3D variants, context extension (PI/NTK/YaRN/DyPE).

## Questions

- [[questions/how-is-mean-flow-time-derivative-computed]] — how is $\mathrm{d}F/\mathrm{d}t$ along the trajectory computed for the Mean Flow loss?
- [[questions/why-cant-cms-use-ode-solvers]] — why are CMs incompatible with standard ODE solvers?
- [[questions/why-does-consistency-training-work-without-teacher]] — why does the same-$\epsilon$ straight-path trick suffice without a teacher?
