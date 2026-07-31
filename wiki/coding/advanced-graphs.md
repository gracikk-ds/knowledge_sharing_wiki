---
Created: 2026-07-04T11:14
Reviewed: Todo
Keywords:
  - leetcode
  - neetcode
  - graphs
  - algorithms
  - shortest path
---
Advanced Graphs на Neetcode — это [[graphs]] плюс веса. В базовом разделе почти всё решалось BFS/DFS, потому что в невзвешенном графе «кратчайший путь» — это число рёбер, и BFS по слоям даёт его бесплатно. Как только у рёбер появляются веса, BFS ломается: путь из трёх лёгких рёбер может быть короче одного тяжёлого, и порядок обхода по слоям больше не совпадает с порядком по стоимости.

Второе отличие — здесь выбор алгоритма определяется свойствами задачи, а не интуицией «обойдём как-нибудь». Перед решением задаём вопросы: веса неотрицательные? есть отрицательные рёбра или ограничение на число шагов? нужен один источник или все пары? нужен путь или дёшево соединить все вершины? Каждый ответ указывает на свой алгоритм — сводка в конце заметки.

## Dijkstra на heap

**Сигнал.** Кратчайший путь из одного источника, веса неотрицательные. «Минимальное время/стоимость добраться до…».

**Идея.** BFS, где очередь заменена на min-[[heap]] по накопленной стоимости. Ключевой инвариант: когда вершина извлекается из heap с минимальным $d$, её расстояние финально — любой другой путь к ней проходит через вершины с $\text{dist} \geq d$, а неотрицательные рёбра могут стоимость только увеличить. Отрицательное ребро ломает именно это «только увеличить» — поэтому Dijkstra требует $w \geq 0$. Вместо decrease-key просто пушим дубликаты и пропускаем устаревшие записи при извлечении.

```python
import heapq

def dijkstra(adj: dict[int, list[tuple[int, int]]], src: int) -> dict[int, int]:
    dist = {src: 0}
    heap = [(0, src)]  # (cost so far, node)
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist.get(u, float("inf")):
            continue  # stale entry, a better path was already found
        for v, w in adj[u]:
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist
```

Для Network Delay Time ответ — $\max$ по `dist.values()`, если достигнуты все $n$ вершин, иначе $-1$.

**Типовые задачи:** Network Delay Time, Path With Minimum Effort.

Сложность: $O(E \log V)$ (с дубликатами в heap формально $O(E \log E)$, что тот же порядок).

## Модифицированный Dijkstra: другая «стоимость пути»

**Сигнал.** Ищем не сумму весов, а другую агрегацию по пути: произведение вероятностей, максимум/минимум веса вдоль пути.

**Идея.** Dijkstra на самом деле не привязан к сумме. Ему нужны два свойства: стоимость пути при добавлении ребра не «улучшается» (монотонность), и мы всегда расширяем лучший из текущих кандидатов. Произведение вероятностей из $(0, 1]$ при добавлении ребра только уменьшается — значит, max-heap по вероятности корректен (в Python — храним отрицание). Minimax-стоимость (Swim in Rising Water: «стоимость пути = максимум значения клетки на нём») при добавлении клетки не уменьшается — min-heap по текущему максимуму финализирует вершины так же честно, как классический Dijkstra по сумме.

```python
def swim_in_water(grid: list[list[int]]) -> int:
    n = len(grid)
    heap = [(grid[0][0], 0, 0)]  # (max cell value on path, r, c)
    seen = {(0, 0)}
    while heap:
        t, r, c = heapq.heappop(heap)
        if r == c == n - 1:
            return t
        for nr, nc in ((r+1, c), (r-1, c), (r, c+1), (r, c-1)):
            if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen:
                seen.add((nr, nc))
                heapq.heappush(heap, (max(t, grid[nr][nc]), nr, nc))
```

**Типовые задачи:** Path with Maximum Probability (произведение, max-heap), Swim in Rising Water (minimax), Path With Minimum Effort (minimax по разнице высот).

Сложность: $O(E \log V)$.

## Bellman-Ford: релаксация по слоям

**Сигнал.** Ограничение на число рёбер в пути («не более $k$ пересадок») или отрицательные веса рёбер.

**Идея.** Relaxation — проход по всем рёбрам с попыткой улучшить $\text{dist}[v]$ через $\text{dist}[u] + w$. Инвариант: после $i$ проходов расстояния корректны для всех путей из не более чем $i$ рёбер. На Cheapest Flights Within K Stops обычный Dijkstra ломается: он финализирует вершину по минимальной стоимости, но дальше может понадобиться более дорогой путь с меньшим числом рёбер — а Dijkstra его уже отбросил. Bellman-Ford перебирает пути ровно по слоям «число рёбер», и снапшот массива обязателен: без копии `prev` одна итерация протаскивает путь сразу через несколько новых рёбер и нарушает лимит $k$.

```python
def cheapest_flights(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    INF = float("inf")
    dist = [INF] * n
    dist[src] = 0
    for _ in range(k + 1):   # path with <= k stops has <= k+1 edges
        prev = dist[:]       # snapshot: relax only against the previous layer
        for u, v, w in flights:
            if prev[u] + w < dist[v]:
                dist[v] = prev[u] + w
    return dist[dst] if dist[dst] < INF else -1
```

Классический Bellman-Ford — то же самое с $V - 1$ итерациями; если на $V$-й итерации что-то ещё улучшается, в графе отрицательный цикл. Тот же слоёный проход можно записать как BFS по состояниям $(\text{вершина}, \text{число шагов})$.

**Типовые задачи:** Cheapest Flights Within K Stops.

Сложность: $O(k \cdot E)$ для версии с лимитом, $O(V E)$ для классической.

## MST: Prim и Kruskal

**Сигнал.** «Соединить все вершины минимальной суммарной стоимостью» — не путь между двумя точками, а остовное дерево.

**Идея.** Обе стратегии опираются на cut property: минимальное ребро через любой разрез графа безопасно добавить в MST. Prim растит одно дерево — как Dijkstra, но в [[heap]] лежит вес одного ребра до вершины, а не накопленная стоимость пути. Kruskal сортирует рёбра по весу и добавляет очередное, если оно соединяет разные компоненты — проверка через union-find из [[graphs]]. Prim удобнее на плотных графах и когда граф задан точками (Min Cost to Connect Points — полный граф, рёбра порождаем на лету); Kruskal — когда рёбра уже даны списком или задача всё равно требует union-find.

```python
def prim_mst(n: int, adj: list[list[tuple[int, int]]]) -> int:
    total, seen = 0, set()
    heap = [(0, 0)]  # (edge weight, node)
    while len(seen) < n:
        w, u = heapq.heappop(heap)
        if u in seen:
            continue
        seen.add(u)
        total += w
        for w2, v in adj[u]:
            if v not in seen:
                heapq.heappush(heap, (w2, v))
    return total

def kruskal_mst(n: int, edges: list[tuple[int, int, int]]) -> int:
    parent = list(range(n))
    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # path halving
            x = parent[x]
        return x
    total = used = 0
    for w, u, v in sorted(edges):  # edges as (weight, u, v)
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            total, used = total + w, used + 1
            if used == n - 1:
                break
    return total
```

**Типовые задачи:** Min Cost to Connect Points, Connecting Cities With Minimum Cost.

Сложность: Prim на heap — $O(E \log V)$, Kruskal — $O(E \log E)$ (доминирует сортировка).

## Eulerian path: алгоритм Хирхольцера

**Сигнал.** «Использовать каждое ребро/билет ровно один раз» — не вершину, а именно ребро.

**Идея.** Жадный DFS с удалением рёбер: идём из вершины, пока есть неиспользованные рёбра, и добавляем вершину в маршрут только когда из неё больше некуда идти (post-order). Тогда «тупиковые» боковые циклы достраиваются рекурсией и оказываются в маршруте до вершин, из которых мы в них свернули; итоговый список разворачиваем. Лексикографически минимальный маршрут в Reconstruct Itinerary получается сортировкой направлений: сортируем в обратном порядке и снимаем `pop()` с конца (или держим heap на каждую вершину).

```python
from collections import defaultdict

def find_itinerary(tickets: list[list[str]]) -> list[str]:
    adj = defaultdict(list)
    for src, dst in sorted(tickets, reverse=True):
        adj[src].append(dst)      # pop() yields the lexically smallest
    route = []
    def dfs(u: str) -> None:
        while adj[u]:
            dfs(adj[u].pop())
        route.append(u)           # post-order: append when stuck
    dfs("JFK")
    return route[::-1]
```

Существование пути в ориентированном графе: ровно одна вершина с $\text{out} - \text{in} = 1$ (старт), ровно одна с $\text{in} - \text{out} = 1$ (финиш), остальные сбалансированы, и все рёбра в одной компоненте.

**Типовые задачи:** Reconstruct Itinerary, Valid Arrangement of Pairs.

Сложность: $O(E \log E)$ на сортировку, сам обход $O(E)$.

## Floyd–Warshall: все пары

**Сигнал.** Нужны кратчайшие расстояния между всеми парами вершин, и $V$ невелико (сотни).

**Идея.** DP по промежуточным вершинам: после итерации $k$ значение $\text{dist}[i][j]$ — кратчайший путь, которому разрешено проходить только через вершины $\{0, \ldots, k\}$. Либо путь вершину $k$ не использует, либо распадается на $i \to k$ и $k \to j$. Работает с отрицательными рёбрами; отрицательный цикл детектируется как $\text{dist}[i][i] < 0$.

```python
def floyd_warshall(dist: list[list[float]]) -> None:
    n = len(dist)  # dist[i][j] = w(i, j) or inf; dist[i][i] = 0
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
```

**Типовые задачи:** Find the City With the Smallest Number of Neighbors at a Threshold Distance.

Сложность: $O(V^3)$ по времени и $O(V^2)$ по памяти — три строки кода против запуска Dijkstra из каждой вершины, при $V \lesssim 400$ это честная сделка.

## Topological sort: Alien Dictionary

**Сигнал.** Порядок элементов нужно восстановить из ограничений «$a$ раньше $b$». Механика — Kahn's algorithm из [[graphs]], здесь добавляется этап построения графа из данных.

**Идея.** В Alien Dictionary граф не дан — его извлекаем из пар соседних слов: первая различающаяся буква даёт ребро $c_1 \to c_2$. Отдельный edge case: если слово — префикс предыдущего (`abc` перед `ab`), порядок противоречив сразу. Дальше стандартный Kahn: очередь вершин с нулевым in-degree; если в итог попали не все вершины — в ограничениях цикл, ответа нет.

**Типовые задачи:** Alien Dictionary, Course Schedule II (из [[graphs]], та же механика).

Сложность: $O(V + E)$ после построения графа.

## Карта раздела

Выбор алгоритма — это ответы на вопросы о графе. Невзвешенный — BFS из [[graphs]]. Веса неотрицательные, один источник — Dijkstra; «стоимость» не сумма, а произведение или минимакс — он же с другой агрегацией. Ограничение на число шагов или отрицательные рёбра — Bellman-Ford. Соединить все вершины дёшево — MST. Все пары на маленьком графе — Floyd–Warshall. Каждое ребро ровно один раз — Eulerian path. Порядок из ограничений — topological sort.

| Алгоритм | Когда применять | Сложность |
|---|---|---|
| BFS ([[graphs]]) | Невзвешенный граф, кратчайший путь по числу рёбер | $O(V + E)$ |
| Dijkstra | Один источник, веса $\geq 0$ | $O(E \log V)$ |
| Модифицированный Dijkstra | Стоимость пути — произведение / минимакс, монотонная | $O(E \log V)$ |
| Bellman-Ford | Отрицательные рёбра или лимит $k$ шагов | $O(V E)$ / $O(k E)$ |
| Prim | MST, плотный граф или граф из точек | $O(E \log V)$ |
| Kruskal | MST, рёбра списком, есть union-find | $O(E \log E)$ |
| Hierholzer | Каждое ребро ровно один раз | $O(E)$ |
| Floyd–Warshall | Все пары, $V \lesssim 400$, можно отрицательные рёбра | $O(V^3)$ |
| Topological sort | Порядок из ограничений-предшествований | $O(V + E)$ |
