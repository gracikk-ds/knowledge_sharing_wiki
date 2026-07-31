---
Created: 2026-07-04T11:13
Reviewed: Todo
Keywords:
  - leetcode
  - heap
  - priority queue
  - algorithms
---
Heap / Priority Queue — класс задач, где из **меняющегося** множества нужно многократно и быстро доставать минимум или максимум. Сигналы: «top-K», «k-th largest/smallest», «в потоке» (данные приходят по одному, ответ нужен после каждого), «самый частый / ближайший / ранний / дешёвый», симуляция событий во времени. Ключевое отличие от полной сортировки: нам не нужен порядок **всех** элементов — только экстремум прямо сейчас, и за это мы платим $O(\log n)$ на операцию вместо $O(n \log n)$ за всё сразу.

Специфика Python: `heapq` — это **только min-heap** поверх обычного `list`. Max-heap делаем инверсией знака (`-x` при push, `-heap[0]` при чтении). Приоритеты с payload — кортежи: сравнение лексикографическое, поэтому `(priority, tiebreak, payload)`; если payload несравним (например, `ListNode`), tiebreak-счётчик обязателен. Peek — просто `heap[0]`, `heapify` строит heap за $O(n)$ (не $O(n \log n)$ — снизу вверх), а `decrease-key` в API нет — вместо него lazy deletion (см. ниже). Для разовых top-K без потока есть однострочники `heapq.nlargest(k, ...)` / `heapq.nsmallest(k, ...)`.

## Heap размера $k$ для top-K / k-th

**Сигнал.** «Найдите $k$ наибольших / ближайших / частых», «$k$-й по величине», особенно когда элементы приходят потоком.

**Идея.** Держим **min**-heap ровно из $k$ элементов — «текущих чемпионов». Корень — слабейший из них, то есть ровно $k$-й по величине: ответ читается за $O(1)$. Новый элемент пушим и, если размер превысил $k$, срезаем корень. Почему не max-heap на все $n$ элементов: это $O(n)$ памяти и $O(n + k \log n)$ времени, а в потоке $n$ вообще не ограничено — min-heap размера $k$ даёт $O(k)$ памяти и $O(\log k)$ на элемент. Для статического массива есть альтернатива — quickselect: в среднем $O(n)$, худший случай $O(n^2)$, зато без дополнительной памяти.

```python
import heapq

class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.heap = nums
        heapq.heapify(self.heap)
        while len(self.heap) > k:
            heapq.heappop(self.heap)

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]  # root of min-heap = k-th largest
```

**Типовые задачи:** Kth Largest Element in a Stream, K Closest Points to Origin (кортежи `(dist, x, y)`), Kth Largest Element in an Array (здесь чаще ждут quickselect), Top K Frequent Elements (частоты из hash map, альтернатива bucket sort — [[arrays-hashing]]).

Сложность: $O(n \log k)$ по времени, $O(k)$ по памяти; quickselect — в среднем $O(n)$.

## Полный heapify + извлечения

**Сигнал.** Симуляция вида «возьми два наибольших, сделай с ними что-то, верни результат обратно»; фиксированного $k$ нет, нужен весь набор.

**Идея.** Превращаем массив в heap целиком за $O(n)$ и дальше просто чередуем pop/push. Это самый «лобовой» паттерн: heap здесь — структура для многократного экстремума, без хитростей. Для максимума — инверсия знака.

```python
import heapq

def last_stone_weight(stones: list[int]) -> int:
    heap = [-s for s in stones]  # max-heap via negation
    heapq.heapify(heap)          # O(n)
    while len(heap) > 1:
        x, y = -heapq.heappop(heap), -heapq.heappop(heap)
        if x != y:
            heapq.heappush(heap, -(x - y))
    return -heap[0] if heap else 0
```

**Типовые задачи:** Last Stone Weight, Furthest Building You Can Reach.

Сложность: $O(n \log n)$ по времени, $O(n)$ по памяти.

## Two heaps: медиана потока

**Сигнал.** Медиана (или иная граница между «половинами») по потоку данных, после каждой вставки.

**Идея.** Разрезаем множество на две половины: max-heap `small` хранит левую (корень — её максимум), min-heap `large` — правую (корень — её минимум). Инвариант: всё в `small` $\leq$ всего в `large`, размеры отличаются не больше чем на 1. Тогда медиана — корень большей половины или среднее двух корней. Балансировка красивая: пушим в одну кучу, тут же перекладываем её корень в другую (это гарантирует порядок между кучами), и если размеры разъехались — возвращаем корень назад.

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.small = []  # max-heap (negated): left half
        self.large = []  # min-heap: right half

    def addNum(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2
```

**Типовые задачи:** Find Median from Data Stream, Sliding Window Median (то же + lazy deletion), IPO (две кучи разной природы: проекты по капиталу и по прибыли).

Сложность: $O(\log n)$ на вставку, $O(1)$ на запрос медианы.

## Heap для симуляции и планирования

**Сигнал.** Задачи/события с приоритетами или временем: «scheduler», «cooldown», «какая задача выполнится следующей», «сколько времени займёт всё».

**Идея.** Heap — это очередь событий: корень всегда говорит, что происходит следующим. В Task Scheduler жадность «выполняй самую частую доступную задачу» реализуется max-heap-ом частот, а cooldown — обычной очередью пар `(ready_time, count)`: задача после выполнения «остывает» и возвращается в heap, когда время подошло. В Single-Threaded CPU наоборот: сортируем задачи по времени прибытия, и в каждый момент кладём все прибывшие в heap с ключом `(processing_time, index)`.

```python
import heapq
from collections import Counter, deque

def least_interval(tasks: list[str], n: int) -> int:
    heap = [-c for c in Counter(tasks).values()]  # max-heap of counts
    heapq.heapify(heap)
    cooldown = deque()  # (ready_time, remaining_count)
    time = 0
    while heap or cooldown:
        time += 1
        if heap:
            cnt = heapq.heappop(heap) + 1  # run one instance
            if cnt:
                cooldown.append((time + n, cnt))
        if cooldown and cooldown[0][0] == time:
            heapq.heappush(heap, cooldown.popleft()[1])
    return time
```

**Типовые задачи:** Task Scheduler, Single-Threaded CPU, Reorganize String, Meeting Rooms II (heap времён окончания — разбор в [[intervals]]).

Сложность: $O(n \log k)$, где $k$ — число различных задач (для букв — константа 26).

## Merge K sorted: heap как фронтир кандидатов

**Сигнал.** $k$ отсортированных источников (списки, строки матрицы, последовательности сумм пар), нужно слить их или найти $m$-й наименьший среди всех.

**Идея.** В heap лежит по **одному** кандидату от каждого источника — «фронтир». Достаём наименьший, тут же пушим его преемника из того же источника. Глобальный минимум всегда на фронтире, поэтому мы ничего не теряем, а heap не растёт больше $k$ — не материализуем все $n \cdot k$ элементов. В K Pairs источник $i$ — это последовательность $\text{nums1}[i] + \text{nums2}[j]$ по $j = 0, 1, \ldots$

```python
import heapq

def k_smallest_pairs(nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
    heap = [(nums1[i] + nums2[0], i, 0) for i in range(min(k, len(nums1)))]
    heapq.heapify(heap)
    res = []
    while heap and len(res) < k:
        _, i, j = heapq.heappop(heap)
        res.append([nums1[i], nums2[j]])
        if j + 1 < len(nums2):
            heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))
    return res
```

**Типовые задачи:** Merge K Sorted Lists (источники — головы списков, кортеж `(val, idx, node)` из-за несравнимых нод; разбор в [[linked-list]]), Find K Pairs with Smallest Sums, Kth Smallest Element in a Sorted Matrix (альтернатива — [[binary-search]] по значению).

Сложность: $O(m \log k)$ на $m$ извлечённых элементов, $O(k)$ по памяти.

## Lazy deletion / hash heap

**Сигнал.** Из heap нужно «удалять» произвольные элементы: элементы устаревают (окно сдвинулось), связи рвутся (unfollow), запись стала неактуальной.

**Идея.** `heapq` не умеет удалять по значению дешевле $O(n)$. Обходим это лениво: удаление — лишь пометка в hash map, а реальная чистка происходит при чтении корня — выкидываем помеченные, пока наверху не окажется живой элемент. Амортизированно каждый элемент пушится и попается один раз, так что асимптотика не портится. В Design Twitter тот же дух доведён до предела: feed собирается merge-ом $k$ отсортированных таймлайнов (фронтир из предыдущей техники), а follow/unfollow правит только hash set фолловеров — из heap вообще ничего не удаляется, он строится заново на каждый запрос.

```python
import heapq
from collections import Counter

class LazyHeap:
    def __init__(self):
        self.heap = []
        self.removed = Counter()  # value -> pending deletions

    def remove(self, x) -> None:
        self.removed[x] += 1      # O(1), defer real work

    def top(self):
        while self.heap and self.removed[self.heap[0]]:
            self.removed[heapq.heappop(self.heap)] -= 1
        return self.heap[0]
```

**Типовые задачи:** Design Twitter, Sliding Window Median, Sliding Window Maximum (альтернатива — monotonic deque, [[sliding-window]]).

Сложность: амортизированно $O(\log n)$ на операцию.

## Heap в Dijkstra

Priority queue пар $(\text{dist}, \text{node})$ с lazy deletion устаревших записей — сердце Dijkstra за $O(E \log V)$; разбор и задачи (Network Delay Time, Swim in Rising Water, Cheapest Flights) — в [[advanced-graphs]].

## Карта раздела

| Техника | Сигнал в задаче | Сложность |
| --- | --- | --- |
| Heap размера $k$ | top-K / $k$-th, поток | $O(n \log k)$ |
| Heapify + извлечения | симуляция «возьми max, верни результат» | $O(n \log n)$ |
| Two heaps | медиана / граница половин потока | $O(\log n)$ на вставку |
| Симуляция / планирование | события с временем и приоритетом, cooldown | $O(n \log k)$ |
| Merge K sorted | $k$ отсортированных источников | $O(m \log k)$ |
| Lazy deletion | удаление произвольных элементов из heap | амортизированно $O(\log n)$ |
| Dijkstra | кратчайшие пути во взвешенном графе | $O(E \log V)$ |
