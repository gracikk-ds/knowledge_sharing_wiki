---
Created: 2026-02-22T19:54
Reviewed: Doing
---
## Why This Matters

At training time, the choice of attention variant shapes model capacity, stability, and how deep the network can scale. At inference time, it dictates memory consumption through the KV-cache, which stores key and value tensors for every prior token. A 128-head model serving long sequences can easily exhaust GPU memory on KV-cache alone, making attention design the single biggest lever for inference cost.

The landscape has moved well beyond the original multi-head formulation. Modern architectures compress, share, gate, and sparsify attention in ways that directly trade capacity for efficiency. Understanding these tradeoffs — and which models chose which — is essential for anyone designing or deploying frontier LLMs.

---

## Core Concepts

### Multi-Head Attention (MHA)

The original transformer attention computes separate query, key, and value projections for every head. Each head attends over the full sequence using scaled dot-product attention:

$$\mathbf{o}_t = \sum_{j=1}^{t} \frac{\exp(\mathbf{q}_t^\top \mathbf{k}_j / \sqrt{d})}{\sum_{l=1}^{t} \exp(\mathbf{q}_t^\top \mathbf{k}_l / \sqrt{d})} \mathbf{v}_j$$

where $\mathbf{q}_t$, $\mathbf{k}_j$, $\mathbf{v}_j$ are the query, key, and value vectors, and $d$ is the head dimension. Each head learns its own subspace of relationships, and their outputs are concatenated and projected back to model dimension. This gives maximum capacity — every head has independent KV parameters — but the KV-cache scales linearly with head count:

$$\text{KV-cache} = 2 \times n_{\text{heads}} \times n_{\text{layers}} \times d_{\text{head}} \times \text{seq\_len}$$

For a model with 128 heads serving long contexts, this becomes the dominant memory bottleneck at inference.

### Multi-Query Attention (MQA)

MQA collapses all KV projections into a single shared pair: every head uses the same keys and values but different queries. This slashes KV-cache by a factor of $n_{\text{heads}}$. The cost is representational — forcing all heads to share the same KV subspace limits what the model can learn. Hugging Face ablations confirmed that MHA outperformed MQA, showing the capacity penalty is real.

### Grouped Query Attention (GQA)

GQA splits heads into small groups (typically 2, 4, or 8) where heads within a group share KV projections. The difference between MHA, GQA, and MQA is best seen as a spectrum of KV sharing:

```jsx
MHA (h=8, no sharing)         GQA (h=8, g=4 groups)        MQA (h=8, 1 shared KV)
┌──┬──┬──┬──┬──┬──┬──┬──┐    ┌──┬──┬──┬──┬──┬──┬──┬──┐    ┌──┬──┬──┬──┬──┬──┬──┬──┐
│Q₁│Q₂│Q₃│Q₄│Q₅│Q₆│Q₇│Q₈│    │Q₁│Q₂│Q₃│Q₄│Q₅│Q₆│Q₇│Q₈│    │Q₁│Q₂│Q₃│Q₄│Q₅│Q₆│Q₇│Q₈│
├──┼──┼──┼──┼──┼──┼──┼──┤    ├──┴──┼──┴──┼──┴──┼──┴──┤    ├──┴──┴──┴──┴──┴──┴──┴──┤
│K₁│K₂│K₃│K₄│K₅│K₆│K₇│K₈│    │ K₁  │ K₂  │ K₃  │ K₄  │    │         K₁            │
├──┼──┼──┼──┼──┼──┼──┼──┤    ├─────┼─────┼─────┼─────┤    ├────────────────────────┤
│V₁│V₂│V₃│V₄│V₅│V₆│V₇│V₈│    │ V₁  │ V₂  │ V₃  │ V₄  │    │         V₁            │
└──┴──┴──┴──┴──┴──┴──┴──┘    └─────┴─────┴─────┴─────┘    └────────────────────────┘
  8 KV pairs (full cache)       4 KV pairs (cache / 2)        1 KV pair (cache / 8)
```

This softens MQA's capacity loss while still compressing the KV-cache substantially. In Hugging Face experiments, GQA with small groups (2/4/8) outperformed MHA on HellaSwag, MMLU, and ARC benchmarks — a striking result suggesting that some KV sharing acts as beneficial regularization. GQA has become the default for most modern models: Trinity Large uses 8 groups, gpt-oss-120b uses 8 groups, SmolLM3 uses 4, and OLMo 3 adopts it as well.

> [!important]
> 
> **Key insight:** GQA with small groups doesn't just save memory — it actually outperformed full MHA in ablations, suggesting that sharing KV across a few heads provides useful inductive bias.

### Multi-Latent Attention (MLA)

Instead of storing full KV tensors per head, MLA compresses them into low-dimensional latent variables and decompresses at runtime. The input is projected down into a small latent:

$$\mathbf{c}_t = \mathbf{W}_{\text{down}} \mathbf{x}_t$$

Only $\mathbf{c}_t$ is cached — at attention time, full keys and values are recovered via upward projections:

$$\mathbf{K}_t = \mathbf{W}_{K}^{\text{up}} \mathbf{c}_t, \quad \mathbf{V}_t = \mathbf{W}_{V}^{\text{up}} \mathbf{c}_t$$

Since $dim(\mathbf{c}_t) ll n_{\text{heads}} \times d_{\text{head}}$, this achieves 4–8x KV-cache compression — comparable to aggressive GQA — while preserving more representational capacity than simple sharing. The tradeoff is implementation complexity: the compression/decompression machinery adds engineering overhead. Kimi-K2 and DeepSeek adopt MLA as their primary attention mechanism.

### Gated Attention

Standard attention can develop "attention sinks" — tokens that accumulate disproportionately high attention weight despite carrying little semantic relevance. Gated attention addresses this by applying an elementwise sigmoid gate to the attention output:

$$\tilde{\mathbf{o}}_{t,i} = \mathbf{o}^{\text{sdpa}}_{t,i} \odot \sigma(\mathbf{W}^G \mathbf{x}_t)$$

where $\mathbf{o}^{\text{sdpa}}_{t,i}$ is the standard scaled dot-product attention output, $\mathbf{W}^G$ is a learned gating matrix, and $\sigma$ is the sigmoid function. The gate learns to suppress uninformative attention patterns, reducing large activations that destabilize training and improving long-sequence generalization.

### Gated Linear Attention (GLA) & Hybrid Models

The key insight behind linear attention is algebraic. Standard attention normalizes over the full sequence via softmax. If we drop the softmax, the sum can be refactored into a recurrent state:

$$\mathbf{o}_t = \sum_{j=1}^{t} (\mathbf{q}_t^\top \mathbf{k}_j) \mathbf{v}_j = \underbrace{\left(\sum_{j=1}^{t} \mathbf{v}_j \mathbf{k}_j^\top\right)}_{S_t} \mathbf{q}_t$$

where $S_t$ is a matrix that accumulates outer products of all past key-value pairs. This gives us $O(1)$ memory per step at inference. But without softmax normalization, the state $S_t$ grows unboundedly. GLA fixes this with a learned forget gate:

$$S_t = G_t \odot S_{t-1} + \mathbf{v}_t \mathbf{k}_t^T$$

where $G_t$ is a gating matrix that controls how much history to retain vs. forget. This formulation supports both parallel (chunked) training and efficient autoregressive inference. In practice, hybrid architectures interleave GLA layers with standard softmax attention layers:

```jsx
Layer 1:  [Softmax Attention]  ← full quadratic, captures precise retrieval
Layer 2:  [GLA / Mamba-2    ]  ← linear recurrence, cheap long-range mixing
Layer 3:  [Softmax Attention]
Layer 4:  [GLA / Mamba-2    ]
  ...
```

Mamba-2 is used in this hybrid pattern within Nemotron-H and Falcon H1, while DeltaNet appears in Qwen3-Next.

### Long-Context Attention Patterns

Full quadratic attention over very long sequences is prohibitively expensive — cost scales as $O(n^2)$ with sequence length $n$. Several patterns reduce this while preserving the information the model needs.

**Sliding Window Attention (SWA)** restricts each token to a fixed window of $p$ positions backward. Gemma 3 combined SWA with full attention every other layer:

```jsx
Causal Full Attention (token 6):     Sliding Window, p=3 (token 6):

  1 2 3 4 5 6  ← keys                 1 2 3 4 5 6  ← keys
1 ■ · · · · ·                       1 · · · · · ·
2 ■ ■ · · · ·                       2 · · · · · ·
3 ■ ■ ■ · · ·                       3 · · · · · ·
4 ■ ■ ■ ■ · ·                       4 · · · ■ · ·
5 ■ ■ ■ ■ ■ ·                       5 · · · ■ ■ ·
6 ■ ■ ■ ■ ■ ■                       6 · · · ■ ■ ■
↑ queries                            ↑ queries
  O(n²) compute                        O(n·p) compute
```

**Dual Chunk Attention (DCA)** divides the sequence into chunks with hierarchical attention: normal attention within chunks, local-window attention between nearby chunks, and broader attention with position caps for distant chunks. Qwen-2.5 used DCA to support context windows of up to 1 million tokens.

**Interleaving local/global attention** alternates restricted-window layers with full-sequence layers. This balances quadratic complexity reduction with long-range dependency preservation. Adjusting the ratio of global layers can aid loss recovery during training instability — increasing their frequency results in quicker loss recovery.

### Document Masking

When multiple documents are packed into a single training sequence for efficiency, standard causal masking lets tokens attend across document boundaries. Document masking restricts attention to tokens within the same document, preventing cross-contamination:

```jsx
Packed sequence: [Doc A tokens | Doc B tokens | Doc C tokens]

Standard causal mask:              Document mask:
  A  A  A  B  B  B  C  C            A  A  A  B  B  B  C  C
A ■  ·  ·  ·  ·  ·  ·  ·          A ■  ·  ·  ·  ·  ·  ·  ·
A ■  ■  ·  ·  ·  ·  ·  ·          A ■  ■  ·  ·  ·  ·  ·  ·
A ■  ■  ■  ·  ·  ·  ·  ·          A ■  ■  ■  ·  ·  ·  ·  ·
B ■  ■  ■  ■  ·  ·  ·  ·          B ·  ·  ·  ■  ·  ·  ·  ·
B ■  ■  ■  ■  ■  ·  ·  ·          B ·  ·  ·  ■  ■  ·  ·  ·
B ■  ■  ■  ■  ■  ■  ·  ·          B ·  ·  ·  ■  ■  ■  ·  ·
C ■  ■  ■  ■  ■  ■  ■  ·          C ·  ·  ·  ·  ·  ·  ■  ·
C ■  ■  ■  ■  ■  ■  ■  ■          C ·  ·  ·  ·  ·  ·  ■  ■
    Doc B attends to Doc A              Each doc isolated
```

SmolLM3 found small improvements on PIQA but otherwise no noticeable impact on short-context tasks. However, document masking became crucial for scaling from 4k to 64k tokens — it provides the clean attention boundaries needed for long-context extension. For smaller models, some teams omit it, judging that the added complexity doesn't justify the benefits at those scales.

---

## How They Compare

### KV-Cache Efficiency vs. Capacity

|Technique|KV-Cache Size|Capacity|Complexity|Used By|
|---|---|---|---|---|
|**MHA**|Full (1 KV per head)|Highest|Standard|—|
|**MQA**|Minimal (1 KV total)|Lowest|Standard|—|
|**GQA** (groups of 2–8)|Reduced by group factor|High (outperforms MHA in ablations)|Standard|Trinity Large, gpt-oss-120b, OLMo 3, SmolLM3|
|**MLA**|4–8x compressed|High|Higher (compression/decompression)|Kimi-K2, DeepSeek|

← less memory … MQA — GQA — MHA … more capacity →

### Long-Context Patterns

|Pattern|Context Reach|Compute Scaling|Used By|
|---|---|---|---|
|**Sliding Window**|Local ( $p$ tokens)|Linear|Gemma 3|
|**Dual Chunk**|Up to 1M tokens|Sub-quadratic|Qwen-2.5|
|**Local/Global Interleaving**|Full (on global layers)|Mixed|Multiple|
|**Document Masking**|Within-document|Same as base|SmolLM3|

---

## In Practice

**Default choice:** Dense model with GQA (4 or 8 groups) and RoPE/RNoPE. This is the most well-understood configuration with strong tooling support (FlashAttention compatibility, straightforward FSDP sharding).

**If you need maximum KV-cache compression** and can invest in implementation: MLA provides 4–8x compression with better capacity preservation than aggressive GQA, but raises engineering complexity. Choose this path only if inference memory is the binding constraint and you have the team to maintain custom kernels.

**For long-context models (64k+ tokens):** Document masking is non-negotiable — SmolLM3 found it crucial for scaling beyond 4k. Combine with RNoPE (alternating RoPE/NoPE layers) or YaRN-style scaling. Consider interleaving local/global attention to manage compute cost.

**Gated attention** is worth adding when training stability is a concern — it reduces attention sinks and large activations with modest parameter overhead.

**Avoid novel attention variants** (GLA hybrids, MLA) unless you have thorough ablation data for your specific scale and task mix. Simpler kernels mean fewer bugs and faster iteration.

**Concrete configurations from frontier models:**

- Kimi-K2: MLA, 384 MoE experts

- Trinity Large: GQA with 8 groups

- gpt-oss-120b: GQA with 8 groups

- SmolLM3: GQA with 4 groups, RNoPE + document masking

---

## Key Takeaways

- GQA with small groups (2–8 heads) is the strongest default — it outperformed MHA in ablations while substantially reducing KV-cache, and is adopted by most frontier models.

- MLA achieves 4–8x KV-cache compression but adds implementation complexity; reserve it for inference-memory-critical deployments.

- Gated attention suppresses attention sinks and stabilizes training — a low-cost addition worth considering for large-scale runs.

- Document masking has minimal impact on short-context tasks but is critical for extending beyond 4k tokens to 64k+.

- For long context, combine document masking with RNoPE or YaRN scaling and consider local/global attention interleaving to manage compute.