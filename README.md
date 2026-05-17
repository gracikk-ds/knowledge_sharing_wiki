# ML Notes Wiki

Личный LLM-поддерживаемый wiki по машинному обучению. Сюда складываются papers, лекции, статьи и записи внутренних knowledge sharings; Claude читает их, разбирает по единому шаблону, иллюстрирует, и складывает в навигируемую сеть страниц. Сайт собирается Quartz и деплоится на Vercel из ветки `main`.

## Что внутри

```
.
├── AGENTS.md             # указатель на .claude/CLAUDE.md
├── README.md             # этот файл
├── ONBOARDING.md         # текстовая шпаргалка; /onboard для интерактивного гида
├── .claude/              # всё, что нужно Claude
│   ├── CLAUDE.md         # главные инструкции
│   ├── role.md           # роль и стиль
│   ├── rules/            # язык, коммиты, иллюстрации, frontmatter
│   ├── agents/           # wiki-source-researcher
│   └── skills/           # wiki-ingest, wiki-query, wiki-lint, wiki-quiz, onboard, autodoc
├── raw/                  # исходники — LOCAL ONLY (gitignored)
│   └── papers/  lectures/  clips/  knowledge-sharings/  scratch/
├── wiki/                 # разборы, один источник = одна страница
│   ├── index.md          # лендинг + Recent / by-kind / by-tag
│   ├── tags.md           # реестр тегов
│   ├── log.md            # chronological event log
│   ├── papers/  lectures/  clips/  knowledge-sharings/
│   └── static/figures/   # PNG: <slug>-<figure>.png
├── publish/              # Quartz, деплоится на Vercel
└── .autodoc/             # сессионная память для LLM
```

`raw/` — локальная папка, **в git не коммитится**. Сами файлы остаются на твоей машине; git хранит только структуру подпапок через `.gitkeep`. На странице разбора записан `source_path` и ссылка на arxiv/блог — этого достаточно, чтобы переcкачать оригинал при необходимости. `wiki/` — пишет Claude через скиллы. `.claude/` — конфигурация.

## С чего начать

Если ты впервые в репо — запусти `/onboard`. Это интерактивный гид, который проведёт по шагам: что лежит в `raw/`, как сделать первый разбор, как закоммитить, как опубликовать. Текстовая версия тех же шагов — в [`ONBOARDING.md`](ONBOARDING.md).

Полные правила и описание шаблонов — в [`.claude/CLAUDE.md`](.claude/CLAUDE.md).

## Основные команды

| Что хочешь | Команда |
|---|---|
| Разобрать один источник | `/wiki-ingest raw/<path>` |
| Спросить wiki по теме | `/wiki-query "<вопрос>"` |
| Проверить wiki перед коммитом | `/wiki-lint` |
| Прогнать себя по теме | `/wiki-quiz <topic>` |
| Записать сессионные инсайты | `/autodoc` |
| Пройти онбординг | `/onboard` |

## Как работает разбор

Один источник → одна страница. Никаких отдельных страниц-концептов: `attention` объясняется внутри разбора Vaswani-2017, `RoPE` — внутри Su-2021. Если по концепту нужно собрать несколько углов — навигация идёт через теги (`wiki/tags.md` + auto-generated `/tags/<slug>`).

Каждая страница следует одному шаблону: TL;DR (4-7 предложений), мотивация с разгоном, идея в одной картинке, разбор по подсекциям с формулами и code-сниппетами, опциональные секции (результаты, сравнение, ограничения), вывод, источник. Минимум картинок: 3 для paper, 2 для лекции, 1 для clip / KS.

## Локальный просмотр

```bash
cd publish
npx quartz build --serve
```

Открой `http://localhost:8080`. Если редактируешь `wiki/`, серверу не нужен ребилд — он подхватит изменения.

## Деплой

Vercel смотрит на ветку `main`. Push в `main` = публикация. Перед push прогоняй `/wiki-lint`.

**Claude может пушить сам** — без отдельного апрува. Force-push и пуш в `main` из feature-ветки всё ещё требуют твоего явного «ок».

## Принципы

1. **Integrate, not summarise.** Каждый новый источник встраивается в существующую сеть через теги и `Связанные разборы`, а не лежит изолированно.
2. **Illustrate non-trivial ideas.** Mermaid, matplotlib, или вырезки из исходника с обязательной атрибуцией. AI-генерация картинок запрещена.
3. **Russian prose, English structure.** Текст на русском, заголовки/slug/теги/frontmatter — английские. Подробности — `.claude/rules/01-language-policy.md`.
4. **Atomic commits ≤ 300 lines.** Conventional commits с scope. Подробности — `.claude/rules/02-commit-policy.md`.
5. **Push разрешён** — Claude может сам делать `git push`. Force-push и пуш в `main` из feature-ветки — только с явным «ок».
