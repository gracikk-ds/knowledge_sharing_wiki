---
title: ML Notes Wiki
Updated: 2026-07-07
---
## Классические модели

- [[linear-models|Линейные модели]] — вывод МНК аналитически (нормальные уравнения, QR/SVD для устойчивости) и через градиентный спуск/SGD, регуляризация L1/L2 (ridge/lasso) и разреживание весов, альтернативные лоссы (MAE, MAPE, Huber), линейная классификация через margin, perceptron loss и hinge loss (SVM), логистическая регрессия через MLE и сигмоиду, многоклассовая классификация (one-vs-all, all-vs-all, softmax regression), масштабируемость через hashing trick и шардированные hash-таблицы.

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

## Coding interview

- [[coding/index|Coding Interview Patterns]] — карта техник по roadmap Neetcode: 18 заметок, у каждой шаблон «сигнал → идея → код → типовые задачи → сложность» и сводная таблица в конце.
- [[arrays-hashing|Arrays & Hashing]] — гайд: устройство hash-таблицы, приём «проход + память об увиденном» с выбором ключа и значения, массив вместо таблицы (counting/bucket sort), карта задач.
- [[two-pointers|Two Pointers]] — указатели с противоположных концов, сортировка с пропуском дубликатов, Container With Most Water, Trapping Rain Water, писатель/читатель in-place, Dutch national flag.
- [[stack|Stack]] — парные структуры, стек с дополнительным состоянием, вычисление выражений, monotonic stack (next greater/smaller, площади), сортировка + стек, стек vs рекурсия.
- [[binary-search|Binary Search]] — бинпоиск как поиск границы монотонного предиката: классика по индексам, first/last true, rotated array, peak, binary search on answer, partition двух массивов.
- [[sliding-window|Sliding Window]] — фиксированное и переменное окно, счётчики частот, бюджет замен, Minimum Window Substring, monotonic deque, приём exactly K = atMost(K) − atMost(K−1).
- [[linked-list|Linked List]] — итеративный reverse, dummy node, fast & slow pointers (алгоритм Флойда), зазор в $n$ узлов, copy with random pointer, LRU Cache, Merge K Sorted Lists.
- [[trees|Trees]] — гайд: определение и виды деревьев, DFS и BFS как единственные два алгоритма раздела, три потока данных в DFS (вверх / вниз / аккумулятор), следствия BST-инварианта, обход как представление дерева, карта задач.
- [[tries|Tries]] — базовый prefix tree, wildcard-поиск через DFS, Word Search II (trie + DFS по доске), бинарный trie для максимального XOR, trie vs hash map.
- [[heap|Heap / Priority Queue]] — heap размера $k$ для top-K, two heaps для медианы, симуляция/планирование, merge K sorted как фронтир кандидатов, lazy deletion.
- [[backtracking|Backtracking]] — шаблон choose → explore → unchoose, subsets, combination sum, permutations, строковые разбиения, Word Search, N-Queens, pruning.
- [[graphs|Graphs]] — гайд: терминология и три способа увидеть граф, DFS/BFS с visited и выбором стартового множества, BFS как кратчайший путь, topological sort, union-find, карта задач.
- [[advanced-graphs|Advanced Graphs]] — Dijkstra и его модификации, Bellman-Ford с лимитом шагов, MST (Prim/Kruskal), Eulerian path (Хирхольцер), Floyd–Warshall, выбор алгоритма по свойствам графа.
- [[dp-1d|1-D Dynamic Programming]] — путь brute force → memoization → bottom-up → $O(1)$ памяти; Fibonacci-паттерн, take/skip, knapsack в 1D, LIS, Word Break, палиндромы.
- [[dp-2d|2-D Dynamic Programming]] — grid DP, две последовательности (LCS, Edit Distance), knapsack 0/1 vs unbounded, state machine DP, interval DP, оптимизация памяти.
- [[greedy|Greedy]] — exchange argument и отличие от DP; Kadane, Jump Game, Gas Station, сортировка + жадный проход, Partition Labels.
- [[intervals|Intervals]] — условие пересечения и выбор ключа сортировки; merge, insert без пересортировки, Meeting Rooms I/II, sweep line, offline-запросы + heap.
- [[bit-manipulation|Bit Manipulation]] — XOR-свёртка, приём Кернигана $n \wedge (n-1)$, DP + биты (Counting Bits), reverse bits, сложение через XOR + перенос, bitmask как множество.
- [[math-geometry|Math & Geometry]] — поворот матрицы, spiral matrix, маркеры в первой строке/столбце, Game of Life в два бита, binary exponentiation, умножение строк, решето Эратосфена.

## Системный дизайн

- [[lesson-1_intro|Урок 1: Где/зачем нужен системный дизайн]] — обзорная карта курса: последовательность тем от требований и нагрузки до баз данных, модульности, масштабирования, отзывчивости, поиска и доп. подсистем.
- [[lesson-2_system-requirements|Урок 2: Требования к системе]] — функциональные и нефункциональные требования (cost, scalability, latency, reliability/durability, availability, consistency), CAP-теорема и PACELC, разбор на типовых сервисах (сокращатель ссылок, автодополнение, облачный диск, Telegram, Twitter, Netflix, такси).
- [[lesson-3_system-load|Урок 3: Расчёт нагрузки на систему]] — воронка от MAU/DAU до RPS с поправкой на peak factor, отдельно пользовательский, сетевой (закон Литтла для соединений, стоимость трафика и CDN), вычислительный (пределы чтения/записи БД) и storage-load (репликация ×3, актуальные цены на диски/RAM с поправкой на дефицит памяти 2025–2026), семишаговый алгоритм оценки на собеседовании и разбор на тех же сервисах.
- [[lesson-4_high-level-design|Урок 4: Высокоуровневый дизайн]] — высокоуровневый дизайн как MVP-уровень архитектуры (front-end/back-end/хранилище, балансировка нагрузки для систем с миллионами пользователей) — база, которую следующие уроки насыщают деталями.
- [[lesson-5_choosing-databases|Урок 5: Выбор подходящих баз данных]] — движки B-tree и LSM, row- vs column-хранение, гарантии ACID/BASE/CAP/PACELC, семейства БД (RDBMS, key-value, wide-column, колоночные, документные, object storage) и алгоритм выбора БД под сервис.
- [[lesson-6_modular-design|Урок 6: Модульный подход к дизайну]] — модульная декомпозиция системы на примере интернет-магазина, очереди сообщений: устройство и сравнение RabbitMQ vs Kafka, проектирование сервиса уведомлений и сервиса бронирования.
- [[lesson-7_scaling|Урок 7: Масштабирование системы]] — балансировка нагрузки, распределение и партиционирование данных, репликация и избыточность, консистентное хеширование — на примере абстрактного «сферического» сервиса.
- [[lesson-8_responsiveness|Урок 8: Повышение отзывчивости]] — кэширование (инвалидация, вытеснение, CDN, Netflix Open Connect), генерация ID записей (UUID, сервис-генератор, подход Twitter), протоколы для реального времени: AJAX polling, long-polling, WebSockets, SSE.
- [[lesson-9_search-subsystems|Урок 9: Подсистемы для поиска]] — автодополнение через префиксное дерево, поиск подстрок (префикс-функция, Ахо-Корасик), полнотекстовый поиск и wildcard matching, геопоиск (GeoHash vs QuadTree), архитектура поисковых подсистем.
- [[lesson-10_additional-subsystems|Урок 10: Дополнительные подсистемы]] — ограничение нагрузки (token bucket, leaky bucket, fixed/sliding window, sliding log), модули защиты (прокси, файрвол), внешние сервисы и подсистемы мониторинга.
- [[lesson-3_homework|Google Meet (домашка к уроку 3)]] — черновик функциональных требований видеозвонков (комнаты, аудио/видео, шаринг экрана, чат) и прикидка DAU/MAU для расчёта нагрузки; нефункциональные требования не дописаны.
- [[amazon|Amazon (домашка, Excalidraw)]] — скетч скоупа и требований для системного дизайна интернет-магазина: функциональные требования (просмотр, поиск, корзина, оплата, заказы) и нефункциональные (latency, availability, consistency).

## Лекции (слайды)

- **Дистилляция** — `distillation/flow-map-models.pdf`: flow-map и few-step дистилляция генеративных моделей.
- **Дистилляция** — `distillation/DMM.pdf`: ODE-free few-step генерация — подходы без численного решения ODE.
- **Метрики** — `metrics/VSR_metrics_pt1.pdf`: метрики качества для задач восстановления видео (часть 1).
- **Метрики** — `metrics/VSR_metrics_pt2.pdf`: метрики качества для задач восстановления видео (часть 2).
- **System design** — `system-design/original_pdfs/lesson-2_system-requirements.pdf`: слайды урока про требования к системе.
- **System design** — `system-design/original_pdfs/lesson-3_system-load.pdf`: слайды урока про расчёт нагрузки.
- **System design** — `system-design/original_pdfs/lesson-4_high-level-design.pdf`: слайды урока про высокоуровневый дизайн.
- **System design** — `system-design/original_pdfs/lesson-5_choosing-databases.pdf`: слайды урока про выбор баз данных.
- **System design** — `system-design/original_pdfs/lesson-6_modular-design.pdf`: слайды урока про модульный подход к дизайну и очереди сообщений.
- **System design** — `system-design/original_pdfs/lesson-7_scaling.pdf`: слайды урока про масштабирование системы.
- **System design** — `system-design/original_pdfs/lesson-8_responsiveness.pdf`: слайды урока про повышение отзывчивости.
- **System design** — `system-design/original_pdfs/lesson-9_search-subsystems.pdf`: слайды урока про подсистемы для поиска.
- **System design** — `system-design/original_pdfs/lesson-10_additional-subsystems.pdf`: слайды урока про дополнительные подсистемы.
