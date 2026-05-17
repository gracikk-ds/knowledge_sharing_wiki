---
title: Tag Registry
ingested: 2026-05-18
---

# Tag Registry

_Last updated: 2026-05-18_ _(added: text-to-image)_

Master tag registry. Every tag used on any wiki page must be defined here first. Quartz builds `/tags/<tag>` pages automatically from frontmatter — this file is the human-readable hub that says what each tag means and links to the auto-generated index.

## How this file works

- One H2 per tag.
- Slug under the H2 (e.g., `Slug: attention`) is the value used in page frontmatter.
- One sentence of definition: when to apply this tag.
- Link to the Quartz tag page that lists every breakdown with that tag.
- When a new tag is needed during `/wiki-ingest`, append a new H2 here in the same commit. Do not invent tags ad-hoc on pages without registering them here.

---

## attention

**Slug:** `attention`

Self-attention, cross-attention, и любые механизмы, где модель явно агрегирует информацию по парам query-key-value. Используй для разборов архитектур и работ, где attention — центральный объект (не как побочная деталь).

[Все разборы →](/tags/attention)

## positional-encoding

**Slug:** `positional-encoding`

Способы внести информацию о позиции токена в attention-модели: sinusoidal, learned, RoPE, ALiBi, NoPE и их вариации.

[Все разборы →](/tags/positional-encoding)

## normalization

**Slug:** `normalization`

LayerNorm, RMSNorm, BatchNorm, GroupNorm и их роль в обучении — где ставится, как влияет на градиенты, как сравнивается с альтернативами.

[Все разборы →](/tags/normalization)

## optimization

**Slug:** `optimization`

Оптимизаторы (SGD, Adam, AdamW, Lion, Shampoo), learning rate scheduling, warmup, gradient clipping — всё, что про «как именно мы делаем шаг по градиенту».

[Все разборы →](/tags/optimization)

## regularization

**Slug:** `regularization`

Dropout, label smoothing, weight decay, stochastic depth, augmentations — методы, которые осознанно ухудшают обучение, чтобы улучшить обобщение.

[Все разборы →](/tags/regularization)

## generative-models

**Slug:** `generative-models`

Модели, которые умеют сэмплить из $p(x)$ или $p(x \mid y)$: GAN, VAE, autoregressive LM, diffusion, flow. Тег-зонтик; для конкретных семейств есть свои теги.

[Все разборы →](/tags/generative-models)

## diffusion

**Slug:** `diffusion`

Диффузионные модели — score matching, DDPM, DDIM, classifier-free guidance, latent diffusion, flow matching как родственное семейство.

[Все разборы →](/tags/diffusion)

## flow-matching

**Slug:** `flow-matching`

Flow matching, rectified flow, continuous normalising flows — обучение векторных полей, которые переносят прайор в распределение данных.

[Все разборы →](/tags/flow-matching)

## variational-inference

**Slug:** `variational-inference`

VI, ELBO, amortised inference, reparameterisation trick, VAE как частный случай. Любые работы, где приближают posterior $q(z \mid x)$ к $p(z \mid x)$.

[Все разборы →](/tags/variational-inference)

## distillation

**Slug:** `distillation`

Knowledge distillation, model compression, teacher-student обучение, distillation в диффузии (consistency models, progressive distillation).

[Все разборы →](/tags/distillation)

## tokenization

**Slug:** `tokenization`

BPE, WordPiece, SentencePiece, byte-level, multimodal tokenization — как сырые данные превращаются в дискретные токены для трансформера.

[Все разборы →](/tags/tokenization)

## inference-economics

**Slug:** `inference-economics`

Стоимость инференса: KV-cache, speculative decoding, quantization, FlashAttention, batching strategies — всё, что про «как сделать дешевле в проде».

[Все разборы →](/tags/inference-economics)

## training-dynamics

**Slug:** `training-dynamics`

Loss landscape, gradient flow, scaling laws, learning rate dynamics, mode collapse — что физически происходит при обучении.

[Все разборы →](/tags/training-dynamics)

## transformer-architecture

**Slug:** `transformer-architecture`

Архитектурные решения внутри трансформера: расположение нормализаций (pre-norm/post-norm), residual, FFN, MoE, MQA/GQA, encoder-decoder vs decoder-only.

[Все разборы →](/tags/transformer-architecture)

## machine-translation

**Slug:** `machine-translation`

NMT, BLEU, parallel corpora, beam search для перевода, BPE для пары языков. Применимо к работам, где машинный перевод — основной бенчмарк или область применения.

[Все разборы →](/tags/machine-translation)

## text-to-image

**Slug:** `text-to-image`

Задача и семейство моделей, генерирующих изображения по текстовому промпту (T2I): SD-серия, FLUX, Imagen, DALL·E, Seedream, Qwen-Image. Не путать с image-editing (TI2I) и с multimodal-understanding (картинка → текст).

[Все разборы →](/tags/text-to-image)
