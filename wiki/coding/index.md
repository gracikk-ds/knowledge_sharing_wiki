---
title: Coding Interview Patterns
Updated: 2026-07-04
---
Карта техник решения задач по [roadmap Neetcode](https://neetcode.io/roadmap): 18 заметок, по одной на узел дерева. Большинство заметок устроены одинаково — для каждой техники раздела: **Сигнал** (как распознать по условию) → **Идея** (почему работает) → шаблон на Python → типовые задачи → сложность; в конце заметки сводная таблица «Карта раздела». Заметки [[trees]], [[arrays-hashing]] и [[graphs]] уже переписаны в формате связного гайда (теория → несколько общих идей с шаблонами → карта задач в конце) — образец, на который постепенно переводятся остальные.

## Базовые структуры

- [[arrays-hashing|Arrays & Hashing]] — гайд: устройство hash-таблицы и откуда берётся $O(1)$; один приём «проход + память об увиденном» с выбором ключа и значения (set, индекс, счётчик, каноническая форма, префиксная сумма); массив вместо таблицы (counting/bucket sort); карта задач.
- [[two-pointers|Two Pointers]] — указатели с противоположных концов, 3Sum с пропуском дубликатов, Container With Most Water, Trapping Rain Water, писатель/читатель in-place, Dutch national flag.
- [[stack|Stack]] — парные структуры, Min Stack, вычисление выражений (RPN), monotonic stack (next greater/smaller, площади в гистограмме), Car Fleet, явный стек vs рекурсия.

## Поиск, окна, списки

- [[binary-search|Binary Search]] — бинпоиск как поиск границы монотонного предиката: классика по индексам, first/last true, rotated array, peak, binary search on answer, partition двух массивов.
- [[sliding-window|Sliding Window]] — фиксированное и переменное окно, счётчики частот, бюджет замен, Minimum Window Substring, monotonic deque, трюк exactly K = atMost(K) − atMost(K−1).
- [[linked-list|Linked List]] — итеративный reverse, dummy node, fast & slow pointers и алгоритм Флойда (с доказательством), зазор в $n$ узлов, Reorder List, copy with random pointer, LRU Cache, Merge K Lists.

## Деревья и кучи

- [[trees|Trees]] — гайд: что такое дерево, виды и роль высоты; DFS и BFS как единственные два алгоритма раздела; три потока данных в DFS (вверх / вниз / аккумулятор); следствия BST-инварианта; обход как представление дерева; карта задач в конце.
- [[tries|Tries]] — базовый prefix tree, wildcard-поиск через DFS, Word Search II (trie + DFS по доске с pruning), бинарный trie для максимального XOR, trie vs hash map.
- [[heap|Heap / Priority Queue]] — heap размера $k$ для top-K, two heaps для медианы, симуляция/планирование (Task Scheduler), merge K sorted как фронтир, lazy deletion.

## Перебор

- [[backtracking|Backtracking]] — шаблон choose → explore → unchoose, subsets, combination sum ($i$ vs $i+1$), permutations, строковые разбиения, Word Search, N-Queens, pruning.

## Графы

- [[graphs|Graphs]] — гайд: терминология и три способа увидеть граф (adjacency list, сетка, состояния); DFS/BFS с visited, BFS как кратчайший путь, стартовое множество как параметр (одна вершина / все источники / граница); topological sort (Kahn, DFS-цвета); union-find; карта задач.
- [[advanced-graphs|Advanced Graphs]] — Dijkstra и его модификации (произведение, минимакс), Bellman-Ford с лимитом шагов, MST (Prim/Kruskal), Eulerian path (Хирхольцер), Floyd–Warshall, выбор алгоритма по свойствам графа.

## Динамическое программирование

- [[dp-1d|1-D Dynamic Programming]] — процесс brute force → memoization → bottom-up → память $O(1)$; Fibonacci-паттерн, take/skip, unbounded и 0/1 knapsack в 1D, LIS, Word Break, два состояния из-за знака, палиндромы.
- [[dp-2d|2-D Dynamic Programming]] — grid DP, две последовательности (LCS, Edit Distance), knapsack 0/1 vs unbounded и порядок циклов, state machine, interval DP (Burst Balloons), матчинг с шаблоном, оптимизация памяти.

## Жадные алгоритмы и интервалы

- [[greedy|Greedy]] — exchange argument и отличие от DP; Kadane, расширение достижимой границы (Jump Game), Gas Station, сортировка + жадный проход, диапазон $[lo, hi]$ вместо перебора, Partition Labels.
- [[intervals|Intervals]] — условие пересечения и выбор ключа сортировки; merge, insert без пересортировки, максимум непересекающихся, Meeting Rooms I/II, sweep line, offline-запросы + heap.

## Биты и математика

- [[bit-manipulation|Bit Manipulation]] — XOR-свёртка, $n \wedge (n-1)$ (Керниган), DP + биты (Counting Bits), reverse bits, сложение через XOR + перенос, bitmask как множество.
- [[math-geometry|Math & Geometry]] — поворот матрицы, spiral matrix, маркеры в первой строке/столбце, Game of Life в два бита, binary exponentiation, работа с цифрами, умножение строк, Евклид и решето.
