---
title: ML Notes Wiki
Updated: 2026-06-20
---
Личная вики по машинному обучению. Каждая страница — самостоятельный разбор одной темы с выводом формул: генеративные модели, устройство трансформеров, system design и т.д. Это и главная страница сайта, и индекс, по которому навыки `wiki-query` и `wiki-quiz` выбирают нужные страницы.

## Генеративные модели

- [[elbo-vae|ELBO и VAE]] — вывод ELBO через неравенство Йенсена, разложение на reconstruction и KL, вариационный EM, амортизация и reparameterization trick.
- [[ddpm|DDPM]] — forward-процесс диффузии, связь с динамикой Ланжевена, denoising score matching, обратный процесс и ELBO через взгляд на диффузию как VAE.
- [[energy-based-models|Energy-based models]] — score-функция, denoising score matching с полным доказательством, динамика Ланжевена и annealed-сэмплирование в NCSN.
- [[classifier-guidance|Classifier guidance]] — вывод classifier guidance и classifier-free guidance через разложение условной score-функции по Байесу с guidance scale.

## Трансформеры

- [[attentions|Attention]] — варианты attention (MHA, MQA, GQA, MLA, gated, linear) и long-context паттерны с разбором trade-off между KV-cache и capacity.
- [[rope|RoPE]] — вывод через матрицы поворота, обобщение на 2D/3D и методы расширения контекста (PI, NTK-aware, YaRN, DyPE).

## Прикладные модели

- [[detr|DETR]] — эволюция DETR-детекторов: недостатки vanilla-версии и их устранение в Deformable, DAB, DN, DINO и CO-DETR.

## Лекции (слайды)

- **Дистилляция** — `distillation/flow-map-models.pdf`: flow-map и few-step дистилляция генеративных моделей.
- **Дистилляция** — `distillation/DMM.pdf`: ODE-free few-step генерация — подходы без численного решения ODE.
- **Метрики** — `metrics/VSR_metrics_pt1.pdf`: метрики качества для задач восстановления видео (часть 1).
- **Метрики** — `metrics/VSR_metrics_pt2.pdf`: метрики качества для задач восстановления видео (часть 2).
- **System design** — `system-design/`: вводный курс из трёх лекций (intro, требования к системе, нагрузка).
