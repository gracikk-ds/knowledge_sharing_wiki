# Wiki Overhaul — Design Spec

**Дата:** 2026-05-17
**Ветка:** `wiki-overhaul`
**Статус:** draft, ждёт ревью пользователя
**Источник:** `tmp/remake_wiki_task.md` (SBER), брейнсторм-сессия от 2026-05-17

---

## TL;DR

Переделать `knowledge_sharing_wiki` так, чтобы:
1. Был единый источник правды о роли автора wiki (`.claude/role.md`).
2. Структура `wiki/` стала иерархической (2 уровня внутри `ml_concepts/` и `methods/`).
3. `CLAUDE.md` стал коротким индексом, регламент уехал в `.claude/rules/`.
4. Появился предсказуемый ingest-флоу с проверкой языка и иллюстрациями.
5. Появился `.autodoc/` для persistent-памяти сессий.
6. Появился `ONBOARDING.md` для новых коллег.
7. Репо стал самодостаточным (не зависел от parent `SBER/.claude/` или Mentoring).

Хуки на push, skill-updater и доработка `wiki-quiz` — следующая итерация, не входят в этот спек.

---

## 1. Scope

### В фундаменте (этот спек)

1. Роль автора wiki — `.claude/role.md`.
2. Новая иерархическая структура `wiki/` + миграция существующих страниц без перерайта текста (флаг `needs_rewrite: true` в frontmatter).
3. Переписанный короткий `CLAUDE.md` (≤ 100 строк) + `AGENTS.md` как short-pointer.
4. `.claude/rules/` — 4 правила, автозагружаются (language policy, commit policy, illustration policy, frontmatter schema).
5. `.claude/agents/wiki-source-researcher.md` — один subagent для research-фазы.
6. `wiki-ingest` v2 — entrypoint с 8 фазами как TodoWrite, читает референсы из `_shared/`.
7. `.claude/skills/_shared/` — `page-templates.md`, `illustration-policy.md`, `russian-style.md`.
8. `autodoc` скилл + `.autodoc/{index.md,insights.md}`.
9. `ONBOARDING.md` для новых коллег.
10. Self-containedness check — проверка, что репо не зависит от внешних `.claude/`.

### Вне фундамента (следующие циклы — см. §10)

- `/wiki-push` — обёртка с гейтами вместо ритуала `git push`.
- Skill-updater (3-фазный safety: predict → review → apply).
- Доработка `wiki-quiz` под новую иерархию.
- Опциональные `/wiki-illustrate`, `/wiki-russian` как отдельные скиллы.

### Граф зависимостей слайсов

```
role.md ─┬─→ CLAUDE.md rewrite ─→ AGENTS.md
         ├─→ _shared/ refs ─┬─→ wiki-ingest v2
         │                  └─→ autodoc skill
         └─→ ONBOARDING.md

structure migration (independent slice, может идти параллельно)
rules/ (independent slice)
```

### Ограничения

- **Ветка:** `wiki-overhaul`. На `main` ничего не пушится.
- **Коммиты:** ≤ 300 строк на коммит (правило из CLAUDE.md проекта). Атомарные.
- **`git push` НЕ выполняется** ни Claude, ни в рамках реализации спека.
- **Язык документации в репо:** английский (по global CLAUDE.md). Этот спек — планировочный артефакт, написан по-русски согласно user feedback.
- **Контент wiki:** проза по-русски, заголовки/слаги/frontmatter/теги по-английски (по rules/01).

---

## 2. Структура директорий

### Целевой layout

```
knowledge_sharing_wiki/
├── CLAUDE.md                        # ≤ 100 строк, индекс + 3-5 принципов
├── AGENTS.md                        # short-pointer на CLAUDE.md (1-2 строки)
├── ONBOARDING.md                    # для новых коллег
├── README.md                        # существует, перепроверяется
├── .autodoc/
│   ├── index.md                     # карта insights с датами
│   └── insights.md                  # сами заметки сессий, append-only
├── .claude/
│   ├── role.md                      # роль автора wiki, один источник истины
│   ├── rules/
│   │   ├── 01-language-policy.md
│   │   ├── 02-commit-policy.md
│   │   ├── 03-illustration-policy.md
│   │   └── 04-frontmatter-schema.md
│   ├── agents/
│   │   └── wiki-source-researcher.md
│   └── skills/
│       ├── _shared/
│       │   ├── README.md            # объясняет on-demand loading
│       │   ├── page-templates.md
│       │   ├── illustration-policy.md   # полный мануал
│       │   └── russian-style.md
│       ├── wiki-ingest/SKILL.md
│       ├── wiki-lint/SKILL.md       # существует, апдейт под новую иерархию
│       ├── wiki-query/SKILL.md      # существует, мелкий апдейт
│       └── wiki-quiz/SKILL.md       # доработка ВНЕ фундамента
├── raw/                              # без изменений
│   ├── papers/
│   ├── clips/
│   ├── lectures/
│   └── scratch/
├── wiki/
│   ├── index.md                      # обновляется под новую структуру
│   ├── log.md                        # без изменений
│   ├── ml_concepts/
│   │   ├── attention/
│   │   │   ├── positional-encodings/
│   │   │   ├── variants/
│   │   │   └── efficiency/
│   │   ├── normalization/
│   │   ├── regularization/
│   │   ├── training-dynamics/
│   │   ├── architectures/
│   │   ├── losses/
│   │   └── embeddings/
│   ├── math_concepts/                # пока плоско
│   ├── methods/
│   │   ├── optimizers/
│   │   ├── attention/
│   │   ├── regularization/
│   │   ├── tokenizers/
│   │   └── inference/
│   ├── topics/                       # narrative primers, плоско
│   ├── sources/                      # плоско
│   └── questions/                    # плоско
└── publish/                          # Quartz, без изменений в этом спеке
```

### Правило глубины

Максимум 2 уровня вложенности внутри `ml_concepts/` и `methods/`. Пример легально: `ml_concepts/attention/rope.md`. Пример нелегально: `ml_concepts/attention/positional/rotary/rope.md`.

### Стартовый набор подпапок

- **`ml_concepts/`**: `attention/`, `normalization/`, `regularization/`, `training-dynamics/`, `architectures/`, `losses/`, `embeddings/`. Внутри `attention/`: `positional-encodings/`, `variants/`, `efficiency/`.
- **`methods/`**: `optimizers/`, `attention/`, `regularization/`, `tokenizers/`, `inference/`.

Авторы добавляют новые подпапки по мере накопления контента (правило записано в роли).

### Миграция существующих страниц

Сейчас в `wiki/ml_concepts/` лежат `attention.md`, `transformer.md` и подобные плоско. План:

1. Создать целевые подпапки.
2. `git mv` существующих файлов:
   - `ml_concepts/attention.md` → `ml_concepts/attention/index.md` (зонтик/обзор)
   - `ml_concepts/transformer.md` → `ml_concepts/architectures/transformer.md`
   - и т.д. — полная карта составляется на этапе writing-plans.
3. Добавить `needs_rewrite: true` в frontmatter всем мигрированным страницам.
4. Прогнать поиск `[[ml_concepts/attention]]` и аналогов, починить ссылки.
5. Обновить `wiki/index.md` под новые пути.
6. Прогнать локальный `quartz build` и убедиться, что страницы видны.

Текст страниц **не переписывается** на этом этапе. Перерайт случится при следующем `/wiki-ingest`, который коснётся этой темы.

### Quartz-совместимость

Quartz рендерит вложенные папки из коробки. `cleanUrls: true` уже включён (коммит 73fa469). На этапе реализации нужно проверить, что `Explorer` plugin корректно сворачивает разделы — может потребовать минимального тюнинга конфига.

---

## 3. Роль, CLAUDE.md, AGENTS.md

### 3.1 `.claude/role.md`

Один файл, читаемый человеком и каждым скиллом явным `Read`. Структура (~80-120 строк):

```markdown
# Wiki Author Role

## Кто ты
LLM-автор персональной ML-wiki. Читаешь источники из `raw/`, пишешь и
поддерживаешь структурированные страницы в `wiki/`. Не суммаризируешь —
интегрируешь в сеть концепт-страниц.

## Что отдаёшь читателю
- Понятное пояснение, а не пересказ статьи.
- Мотивированное построение: чего хотим → наивное решение → почему ломается → 
  что предлагает концепт.
- Иллюстрации к каждой нетривиальной идее (mermaid / matplotlib / вырезка).
- Прямой текст, без хеджирования.

## Голос
- Прямой, спокойный, без хайпа.
- Без англицизмов кальками («бэкпропагейтить», «энкодить», «лосс падает»).
  Используй устоявшийся русский ML-словарь: обратное распространение, кодировать,
  функция потерь. Английский остаётся для имён собственных (Transformer, RoPE)
  и заголовков/слагов/тегов.
- Без AI-speak: «давайте», «итак», «в данной статье», «как видно», «стоит отметить».
- Без научного канцелярита: «осуществляется», «представляет собой», «является».
- Без метафор-натяжек.

## Чего НЕ делаешь
- Не правишь `raw/`. Источники immutable.
- Не пишешь без иллюстрации, если концепт нетривиален.
- Не выдумываешь факты. Если в источнике пробел — отдаёшь research-агенту 
  или спрашиваешь пользователя.
- Не пишешь стену в 2000 слов. Длина диктуется содержанием.

## Когда в сомнении
- Концепт спорный → секция «Открытые вопросы» на странице или файл в `questions/`.
- Текст не идёт → пишешь стаб со ссылками, оставляешь `status: stub`.
- Источник конфликтует с тем что в wiki → отмечаешь обе версии с атрибуцией,
  не переписываешь молча.

## Когда добавлять новую подпапку
В `ml_concepts/<top>/<sub>/` — когда в существующих подпапках накапливается 
5+ страниц одной темы и появляется естественная граница (например, в 
`attention/` накопилось 5 page-encodings — выделить `positional-encodings/`).
```

Конкретные формулировки и полный список запрещённых англицизмов добиваются при реализации.

### 3.2 Переписанный `CLAUDE.md` (≤ 100 строк)

```markdown
# CLAUDE.md — ML Notes Wiki

Персональная LLM-wiki по machine learning. Читаешь raw-источники, 
интегрируешь знания в структурированную сеть страниц.

## Первое что прочитать
1. `.claude/role.md` — кто ты и как пишешь
2. `.claude/rules/` — автозагружается, регламент
3. `wiki/index.md` — что уже есть
4. `.autodoc/index.md` — insights прошлых сессий

## Что куда лежит
[короткое дерево, 15-20 строк]

## Слои
- `raw/` — источники, immutable, не правишь
- `wiki/` — пишешь и поддерживаешь
- `.claude/` — конфиг, читаешь, обсуждаешь изменения

## Команды
| Что хочу | Команда |
|---|---|
| Внести статью | /wiki-ingest <путь> |
| Поискать | /wiki-query <вопрос> |
| Проверить wiki | /wiki-lint |
| Закрыть сессию | /autodoc |

## Принципы
1. Интеграция, а не суммаризация.
2. Mermaid + matplotlib + вырезки. AI-генерация картинок запрещена (rules/03).
3. Русский в прозе, английский в заголовках/слагах/frontmatter (rules/01).
4. Коммит ≤ 300 строк (rules/02). Без `git push` без явного OK.

## Деплой
Quartz + Vercel. См. `publish/README.md` и `vercel.json`.
```

### 3.3 `AGENTS.md`

Short-pointer файл, 1-2 строки. Содержание:

```markdown
# AGENTS.md

See `CLAUDE.md` — single source of truth for AI-agent instructions in this repo.
```

Без symlink. Без копии. Указатель.

---

## 4. Карта скиллов и как их запускать

### Финальный набор скиллов

| Скилл | Slash-команда | Когда вызывать | Что делает |
|---|---|---|---|
| `wiki-ingest` | `/wiki-ingest <path>` | Прислали статью / новость / лекцию | Главный флоу: статья → разбор + иллюстрации |
| `wiki-query` | `/wiki-query <вопрос>` | Хочу спросить wiki | Ищет ответ в `wiki/`, ссылки на страницы |
| `wiki-lint` | `/wiki-lint` | Перед коммитом | Чинит frontmatter, битые ссылки, проверяет схему |
| `wiki-quiz` | `/wiki-quiz <topic>` | Проверить знания | Доработка вне фундамента |
| `autodoc` | `/autodoc` | В конце сессии | Собирает insights в `.autodoc/insights.md` |

### Агент (вызывается изнутри скилла)

| Агент | Кем вызывается | Что делает |
|---|---|---|
| `wiki-source-researcher` | `wiki-ingest` фаза 3 | Достаёт из интернета уточнения по пробелам в источнике |

### Правила (автозагружаются)

- `01-language-policy.md`
- `02-commit-policy.md`
- `03-illustration-policy.md`
- `04-frontmatter-schema.md`

### Референсы (читаются по требованию)

- `_shared/page-templates.md`
- `_shared/illustration-policy.md` — полный мануал
- `_shared/russian-style.md`
- `.claude/role.md`

### Граф зависимостей

```
/wiki-ingest ──┬─→ читает .claude/role.md
               ├─→ читает _shared/page-templates.md
               ├─→ читает _shared/russian-style.md
               ├─→ читает _shared/illustration-policy.md
               ├─→ зовёт wiki-source-researcher (фаза 3, опционально)
               └─→ финальная фаза: советует /wiki-lint, /autodoc

/wiki-query  ──→ читает .claude/role.md, wiki/index.md
/wiki-lint   ──→ читает rules/04-frontmatter-schema.md
/wiki-quiz   ──→ читает .claude/role.md (доработка вне фундамента)
/autodoc     ──→ читает .autodoc/index.md, пишет в .autodoc/insights.md
```

### Onboarding-чеатшит из 4 команд

```
1. Прислали статью?   /wiki-ingest raw/papers/название.pdf
2. Хочешь что-то найти? /wiki-query "вопрос"
3. Перед коммитом?      /wiki-lint
4. В конце сессии?      /autodoc
```

Эти 4 команды покрывают 95% работы.

---

## 5. Walkthrough `wiki-ingest` фаза-за-фазой

Пример: пользователь прислал статью про RoPE.

**Команда:** `/wiki-ingest raw/papers/su-2021-roformer.pdf`

### Фаза 1 — Pre-flight (Read'ы)

Скилл читает первым делом:
- `.claude/role.md`
- `_shared/page-templates.md`
- `_shared/russian-style.md`
- `_shared/illustration-policy.md`
- `wiki/index.md`

Создаёт TodoWrite на оставшиеся 7 фаз.

### Фаза 2 — Чтение источника

- Читает PDF целиком (длинные — постранично через `pages`).
- Идентифицирует load-bearing картинки.
- Скаит `wiki/ml_concepts/attention/` — что обновить, что создать.

### Фаза 3 — Уточнение данных (опционально)

Если в источнике пробел, мешающий понятному объяснению, — зовёт `wiki-source-researcher` с конкретным запросом. Агент возвращает структурированный отчёт. Отчёт остаётся в контексте.

Если пробелов нет — фаза пропускается.

### Фаза 4 — Takeaways + согласование

Скилл выводит:

```
Source: RoFormer — Su et al. (paper, 2021)

Takeaways:
- RoPE кодирует позицию через вращение Q/K-векторов.
- dot(q_m, k_n) зависит только от (m - n).
- Совместимо с linear attention и FlashAttention.
- Эмпирически лучше Sinusoidal на длинных контекстах.

Likely wiki impact:
- Create: ml_concepts/attention/positional-encodings/rope.md
- Update: ml_concepts/attention/positional-encodings/index.md
- Stub: ml_concepts/attention/positional-encodings/shaw-relative.md
- Source: sources/su-2021-roformer.md

Открытые вопросы:
- Как RoPE взаимодействует с DyPE/YARN — в paper нет.

Хочешь что-то подчеркнуть или пропустить? Иначе пишу.
```

**Останавливается и ждёт.** Пользователь даёт ОК или правки.

### Фаза 5 — Написание текста

Для каждой страницы:
1. Создаёт/обновляет по шаблону из `_shared/page-templates.md`.
2. Проза на русском, заголовки/слаги/теги на английском.
3. Frontmatter по `rules/04`.
4. Линкует `[[math_concepts/...]]` вместо разворачивания математики inline.
5. Stub-ссылки на не-существующие страницы — оставляет с пометкой.

### Фаза 6 — Иллюстрации

Для каждой нетривиальной идеи:
- **Mermaid** — inline в md.
- **Matplotlib** — `publish/static/figures/<page-slug>/*.py` + `.png`. Скрипт коммитится.
- **Вырезка** — `publish/static/figures/<page-slug>/source-cut-*.png` + атрибуция.

Если идея сложно представляется визуально — стаб-вопрос «как это нарисовать» в `questions/`.

### Фаза 7 — Самопроверка + русский

Скилл повторно читает `_shared/russian-style.md` и проходит чеклист:
- Нет англицизмов-калек.
- Нет AI-speak.
- Каждое утверждение опирается на источник или помечено как открытый вопрос.
- Математика линкуется в `math_concepts/`.
- Иллюстрации привязаны к тексту.

Правит на месте.

### Фаза 8 — Bookkeeping + предложение коммита

1. Обновляет `wiki/index.md`.
2. Дописывает в `wiki/log.md`.
3. Сообщает: список изменённых файлов, новые стабы, противоречия.
4. Предлагает `/wiki-lint`.
5. Предлагает атомарный коммит:
   ```
   feat(wiki): ingest RoFormer (RoPE) — Su et al. 2021

   - new: ml_concepts/attention/positional-encodings/rope.md
   - new: sources/su-2021-roformer.md
   - update: ml_concepts/attention/positional-encodings/index.md
   - figures: publish/static/figures/rope/{rotation-2d.py,rotation-2d.png}
   ```
6. **Не делает `git push`. Никогда.**

### Гейты ожидания пользователя

| Фаза | Чего ждёт |
|---|---|
| 4 | OK на takeaways перед написанием |
| 7 | (опц., режим `--review`) — diff страницы перед фиксацией |
| 8 | OK на текст коммита перед `git commit` |

В автономном режиме фаза 4 эмитит takeaways в чат, но не ждёт. Фазы 7-8 идут без подтверждения.

---

## 6. Политика иллюстраций

Два файла: `rules/03-illustration-policy.md` (короткий регламент, автозагружается) и `_shared/illustration-policy.md` (полный мануал, читается фазой 6 ingest-флоу).

### Разрешено

| Инструмент | Когда | Где живёт |
|---|---|---|
| Mermaid | Архитектуры, потоки, отношения | Inline в md |
| Matplotlib | Графики, плоты, визуализация формул | `publish/static/figures/<page-slug>/*.py` + `.png` |
| Numpy/Torch + matplotlib | Численные примеры | То же |
| Вырезка из источника | Сложная схема, лучше любой реплики | `publish/static/figures/<page-slug>/source-cut-*.png` |

### Запрещено

- **AI-генерация изображений** (DALL·E, SD, Midjourney). Цена ошибки выше пользы.
- **Excalidraw / ручной SVG** в авто-флоу. Только отдельным ручным коммитом.
- **TikZ/LaTeX-фигуры** — overkill для Quartz, ломкий рендер.
- **Скриншоты слайдов без атрибуции.**

### Правила оформления

1. Подпись обязательна:
   - Mermaid: `*Схема: <что показано>*`
   - Matplotlib: `*Сгенерировано: figures/<slug>/<file>.py*`
   - Вырезка: `*Из <First Author> et al. (<year>), Fig. <N>.*`
2. Matplotlib-скрипт коммитится **вместе с PNG** (воспроизводимость).
3. PNG ≤ 200 KB.
4. Имена файлов: kebab-case, без пробелов.
5. Один figures-каталог на страницу.
6. Mermaid: ≤ 12 узлов. Больше — разбить на 2 или matplotlib.

### Чеклист фазы 6 (короткий, для `_shared/illustration-policy.md`)

```
[ ] Каждый нетривиальный концепт имеет иллюстрацию
[ ] Mermaid выбран только для flow/relations
[ ] Matplotlib-скрипт коммитится вместе с PNG
[ ] Вырезки имеют атрибуцию автора и фигуры
[ ] Подпись под каждой картинкой
[ ] Никаких AI-генераций
[ ] PNG ≤ 200 KB
```

---

## 7. autodoc + `.autodoc/`

### Структура

```
.autodoc/
├── index.md       # карта insights: дата + 1-строчный заголовок + ссылка
└── insights.md    # сами insights, append-only
```

### Что записывается

- **Discovery** — что выяснили про предметную область.
- **Wiki structure** — наблюдение про саму wiki (например: «пора выделить подпапку»).
- **Skill/tool issue** — что-то сломалось или плохо сработало.
- **Gotcha** — неочевидная ловушка.

### Что НЕ пишется

- Контент wiki.
- Дублирование того, что в git log.
- TODO-листы текущей сессии (это для TodoWrite).

### Скилл `autodoc`

Порт паттерна из Mentoring. SKILL.md ~80 строк. Логика:

1. Pre-flight: читает `.autodoc/index.md`.
2. Анализирует текущую сессию.
3. Формирует кандидатов в insights (3-7 пунктов).
4. Показывает на ревью.
5. После ОК — append в `insights.md`, апдейт `index.md`.
6. Предлагает коммит: `chore(autodoc): session insights — YYYY-MM-DD`.

### Когда вызывать

- В конце сессии.
- После крупного `/wiki-ingest`, если выяснилось что-то неожиданное.
- При смене темы.

### Чтение autodoc на старте

Автоматизируется через `CLAUDE.md` (не через хук). Блок в `CLAUDE.md`:

```markdown
## Контекст прошлых сессий
Перед нетривиальной работой прочитай `.autodoc/index.md` — там insights 
от прошлых сессий, которые могут сэкономить тебе час.
```

---

## 8. ONBOARDING.md, Commit Policy, Self-Containedness

### 8.1 `ONBOARDING.md`

~120-180 строк. Структура:

- **Что это** (1 абзац)
- **Первый день — 30 минут** — что прочитать по шагам
- **Как ты обычно работаешь** — 4 команды цикла
- **Гейты ожидания пользователя**
- **Чего Claude никогда не делает сам** (push, удаление raw, AI-картинки, коммит > 300 строк)
- **Гид по структуре wiki** — карта подпапок
- **Где править регламент** — где роль, где правила, где шаблоны
- **Локальный preview Quartz** — команда
- **Деплой** — Vercel + main = публикация
- **Куда писать вопросы** — `wiki/questions/`

### 8.2 `rules/02-commit-policy.md`

Берётся за основу из Mentoring, адаптируется:

```markdown
# Commit Policy

## Размер
- ≤ 300 changed lines per commit.
- Больше — атомарные: миграция / новые страницы / иллюстрации отдельно.

## Формат
Conventional commits:
- `feat(wiki): ingest <source> — <short-desc>`
- `feat(wiki): add page <slug>`
- `fix(wiki): broken link in <file>`
- `refactor(wiki): move <files> to <new-path>`
- `chore(autodoc): session insights — YYYY-MM-DD`
- `docs(skill): update wiki-ingest phase 4`

## Что коммитим / нет
- `.autodoc/` — коммитим
- `publish/node_modules/`, `publish/.quartz-cache/` — gitignore
- `raw/*` — коммитим
- PNG > 200 KB — отказ

## Push policy
- Claude никогда не делает `git push` сам.
- Push делает только пользователь, явно.
- На main = деплой Vercel. Перед push — `/wiki-lint`.

## Ветки
- `main` — то, что деплоится.
- Любые крупные изменения → отдельная ветка.
- Мелкие опечатки — можно в main.
```

### 8.3 Self-containedness check

Требование: репо не зависит от родительских `.claude/` (SBER, Mentoring).

**Чеклист (часть финальной фазы реализации):**

```
[ ] grep -r "/Users/" .claude/ wiki/ CLAUDE.md AGENTS.md ONBOARDING.md → 0 матчей
[ ] grep -r "Mentoring" .claude/ → 0 матчей
[ ] grep -r "course\|студент\|ментор\|курс" .claude/ → 0 матчей
[ ] Все Read в SKILL.md идут на относительные пути внутри репо
[ ] AGENTS.md — short-pointer, без external refs
```

**Скопированные паттерны из Mentoring/SBER** копируются с адаптацией под ML-wiki, без упоминаний менторства/курсов/преподавания.

**Запись в ONBOARDING.md и CLAUDE.md:** «Открывай этот репо как самостоятельный workspace, не из SBER, чтобы parent CLAUDE.md из SBER не подгружался.»

---

## 9. Verification

### Smoke tests

**1. Структурный sanity**
```
[ ] wiki/ml_concepts/, methods/ имеют ≥ 1 подпапку
[ ] Глубина вложенности ≤ 2 уровня
[ ] Каждый файл md в wiki/ имеет валидный frontmatter (по rules/04)
[ ] wiki/index.md покрывает все существующие страницы
[ ] Нет битых [[wiki-links]] (lint-проход)
[ ] cd publish && npx quartz build → без ошибок
```

**2. Скиллы загружаются**
```
[ ] /wiki-ingest <known-file> проходит фазу 1
[ ] /wiki-query <known-question> возвращает результат
[ ] /wiki-lint выполняется без падений
[ ] /autodoc проходит фазу планирования
```

**3. Самодостаточность**
```
[ ] grep -r "/Users/" → 0 матчей в .claude/ и корневых md
[ ] grep -r "Mentoring\|менторинг" .claude/ → 0 матчей
[ ] Открыть репо как отдельный workspace, /wiki-query — работает
```

**4. End-to-end ingest**

Взять одну реальную статью (clip или paper из существующего `raw/`), прогнать `/wiki-ingest` до коммита. Проверить:
- Страница создана с правильным frontmatter.
- Mermaid рендерится в локальном Quartz preview.
- Русский без англицизмов.
- Иллюстрация на месте, скрипт matplotlib коммитится.
- `sources/*.md` создан.
- `index.md` и `log.md` обновлены.

### Definition of Done

```
[ ] Ветка wiki-overhaul, ≥ 10 атомарных коммитов (≤ 300 строк каждый)
[ ] Все 4 smoke-tests группы зелёные
[ ] One realистичный source прогнан через /wiki-ingest до коммита
[ ] CLAUDE.md ≤ 100 строк
[ ] ONBOARDING.md существует и читается за 30 минут
[ ] .autodoc/{index.md,insights.md} существуют с минимум одной записью
[ ] git push НЕ выполнялся
```

### Что НЕ верифицируем в фундаменте

- Работу хуков на push (их нет).
- Skill-updater (его нет).
- Работу quiz на новой структуре.

---

## 10. Next iteration (вне фундамента)

Дизайн верхнего уровня для следующих циклов, чтобы хуки и доработки не потерялись.

### 10.1 `/wiki-push` — обёртка push с гейтами

Скилл, заменяющий ритуал `git push`:

1. Pre-flight: проверка ветки, `git status` clean.
2. `/wiki-lint` — если падает, стоп.
3. `/autodoc` — собрать insights.
4. Diff `.claude/skills/`, `.claude/role.md`, `.claude/rules/` за сессию — если есть, фаза skill-update (см. 10.2).
5. Summary: что коммитится, что Vercel задеплоит.
6. Дождаться `OK push`.
7. `git push`.

Не git pre-push hook. Альтернативная команда вместо `git push`.

### 10.2 Skill-updater

Безопасный 3-фазный апдейт скиллов/роли/правил:

1. **Predict.** На основе `.autodoc/insights.md` за последние N сессий — diff на `.claude/role.md`, `_shared/*.md`, `SKILL.md`. Diff кладётся в `.claude/proposed-changes/<date>.diff`, оригиналы **не правятся**.
2. **Review.** Пользователь смотрит diff руками, помечает accepted hunks (комментарий `# accepted`).
3. **Apply.** Скилл применяет accepted hunks, удаляет diff-файл, коммит `chore(meta): apply skill updates from <date>.diff`.

LLM не редактирует свои инструкции автономно. Все изменения через явный ревью.

### 10.3 Доработка `wiki-quiz`

- Адаптация под иерархическую структуру (`/wiki-quiz attention/positional-encodings`).
- Режим «слепой проверки» — пользователь отвечает не глядя.
- Логирование результатов в `wiki/quiz-log.md` или `.autodoc/`.

### 10.4 Опциональные улучшения

- `/wiki-illustrate <page>` — перерисовать/добавить иллюстрации к существующей странице.
- `/wiki-russian <page>` — языковая чистка существующей страницы.
- Git pre-commit hook (стандартный shell-скрипт) — frontmatter валидность, размер коммита.

### Порядок реализации после фундамента

1. `/wiki-push` минимальный (без skill-updater).
2. Skill-updater (3-фазный safety).
3. `/wiki-push` фаза 4 (интегрировать skill-updater).
4. `/wiki-quiz` доработка.
5. Опциональные скиллы.

Каждый пункт — отдельный спек + writing-plans цикл.

---

## Открытые вопросы и допущения

### Допущения

- Quartz `Explorer` plugin корректно сворачивает вложенные разделы (проверить на этапе реализации, при необходимости — мини-патч конфига).
- `git mv` сохранит историю файлов и не сломает blame.
- Vercel не имеет особых правил на структуру `publish/content/` сверх того, что есть в `publish/quartz.config.ts`.

### Открытые вопросы (на ревью)

- Нужен ли в `.claude/role.md` явный список запрещённых англицизмов или достаточно общего правила? — Предлагаю короткий список (10-15 примеров) в роли, расширяемый по мере накопления.
- Нужен ли скилл `wiki-illustrate` уже в фундаменте или в следующей итерации? — Спек ставит его в next iteration. Если выяснится, что иллюстрации часто требуют отдельной итерации без полного `/wiki-ingest` — поднять в фундамент.
- Где жить роли — `.claude/role.md` или `.claude/skills/_shared/role.md`? — Спек ставит на `.claude/role.md` (короткий путь, легко референсить). Альтернатива симметрично работоспособна.

---

## Приложение: список файлов, создаваемых/изменяемых спеком

### Новые файлы

- `CLAUDE.md` (перепись)
- `AGENTS.md`
- `ONBOARDING.md`
- `.autodoc/index.md`
- `.autodoc/insights.md`
- `.claude/role.md`
- `.claude/rules/01-language-policy.md`
- `.claude/rules/02-commit-policy.md`
- `.claude/rules/03-illustration-policy.md`
- `.claude/rules/04-frontmatter-schema.md`
- `.claude/agents/wiki-source-researcher.md`
- `.claude/skills/_shared/README.md`
- `.claude/skills/_shared/page-templates.md`
- `.claude/skills/_shared/illustration-policy.md`
- `.claude/skills/_shared/russian-style.md`
- `.claude/skills/wiki-ingest/SKILL.md` (перепись)

### Изменяемые файлы

- `.claude/skills/wiki-lint/SKILL.md` (мелкий апдейт под новую иерархию и `rules/04`)
- `.claude/skills/wiki-query/SKILL.md` (мелкий апдейт — читать `.claude/role.md`)
- `wiki/index.md` (под новую иерархию)
- `README.md` (перепроверка)

### Файлы которые двигаются

- `wiki/ml_concepts/*.md` → `wiki/ml_concepts/<topic>/{*.md|index.md}` (полная карта — на этапе writing-plans)
- `wiki/methods/*.md` → `wiki/methods/<topic>/*.md`

### Файлы которые НЕ трогаем

- `raw/**`
- `publish/**` (за исключением добавления `publish/static/figures/<page-slug>/*` при первом ingest)
- `vercel.json`
- `wiki/log.md` (только append через ingest)
- `wiki/sources/`, `wiki/questions/`, `wiki/topics/` (плоско, не мигрируем)
