---
Created: 2026-07-04T11:12
Reviewed: Todo
Keywords:
  - leetcode
  - neetcode
  - binary search
  - algorithms
---
Binary Search на Neetcode — раздел про задачи, где пространство поиска сокращается вдвое за шаг. Наивный взгляд — «бинпоиск ищет элемент в отсортированном массиве» — покрывает только первую задачу раздела и мешает узнавать остальные.

Главный обобщающий взгляд: бинпоиск работает по любому монотонному predicate, а не по «отсортированному массиву». Если на пространстве поиска есть функция $p(x)$, которая выглядит как `F F F T T T` (единственный переход false $\to$ true), то бинпоиск находит границу за $O(\log n)$ — независимо от того, что это за пространство: индексы массива, скорости поедания бананов или позиции разреза. Отсортированный массив — частный случай с predicate $p(i) = (a_i \geq \text{target})$. Почти каждая техника ниже — просто другой выбор пространства и predicate.

## Классический бинпоиск по индексам

**Сигнал.** Отсортированный массив, ищем точное вхождение target.

**Идея.** Invariant: если target есть в массиве, он лежит в $[\text{left}, \text{right}]$. Сравнение с серединой отбрасывает половину. Шаблон `left <= right` с шагами `mid + 1` / `mid - 1` — окно честно сужается, цикл не зависает. В C++/Java `left + right` может переполниться, поэтому там пишут `left + (right - left) / 2`; в Python `int` произвольной точности, так что $(l + r) / 2$ безопасно всегда.

```python
def search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2  # no overflow in Python
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

**Типовые задачи:** Binary Search, Guess Number Higher or Lower.

Сложность: $O(\log n)$.

## Поиск границы: first true / last true

**Сигнал.** «Первое/последнее вхождение», «позиция вставки», «наименьший $x$, такой что…» — нужен не элемент, а граница перехода predicate.

**Идея.** Это каноническая форма бинпоиска, к которой сводится всё остальное. Шаблон `left < right`: если $p(\text{mid})$ истинен, mid может быть ответом — сохраняем его через `hi = mid`; если ложен — точно нет, `lo = mid + 1`. Цикл сходится ровно к первому true. Last true — это first true минус один. В стандартной библиотеке то же самое делают `bisect_left` (первый индекс с $a_i \geq \text{target}$) и `bisect_right` (первый с $a_i > \text{target}$).

```python
def first_true(lo: int, hi: int, pred) -> int:
    # smallest x in [lo, hi] with pred(x); returns hi + 1 if none
    while lo < hi:
        mid = (lo + hi) // 2
        if pred(mid):
            hi = mid       # mid may be the answer, keep it
        else:
            lo = mid + 1   # mid is definitely not
    return lo

first = bisect_left(nums, target)        # first i: nums[i] >= target
last = bisect_right(nums, target) - 1    # last  i: nums[i] <= target
```

**Типовые задачи:** Find First and Last Position of Element in Sorted Array, Search Insert Position, First Bad Version.

Сложность: $O(\log n)$.

## Rotated sorted array

**Сигнал.** «Отсортированный массив, повёрнутый вокруг неизвестного pivot».

**Идея.** Массив глобально не отсортирован, но в любой точке разреза хотя бы одна половина отсортирована — это проверяется сравнением концов. Для поиска target: определяем отсортированную половину, смотрим, попадает ли target в её диапазон, и отбрасываем другую. Для минимума predicate ещё проще: сравниваем `nums[mid]` с правым концом — если больше, точка поворота (и минимум) строго правее.

```python
def find_min(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:  # min is strictly to the right
            left = mid + 1
        else:                        # mid itself may be the min
            right = mid
    return nums[left]
```

**Типовые задачи:** Search in Rotated Sorted Array, Find Minimum in Rotated Sorted Array; с дубликатами (Search in Rotated Sorted Array II) худший случай деградирует до $O(n)$.

Сложность: $O(\log n)$.

## Поиск peak: бинпоиск по «наклону»

**Сигнал.** Массив не отсортирован, но нужен любой локальный максимум, и сравнение соседей подсказывает направление.

**Идея.** Хороший тест на понимание: сортировки нет вообще, а бинпоиск работает. Predicate — «мы на подъёме»: если $\text{nums}[\text{mid}] < \text{nums}[\text{mid}+1]$, справа гарантированно есть peak (подъём обязан где-то закончиться), идём вправо; иначе peak — сам mid или левее. Достаточно любого правила, которое безопасно отбрасывает половину.

```python
def find_peak(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < nums[mid + 1]:  # ascending slope: peak is to the right
            lo = mid + 1
        else:
            hi = mid
    return lo
```

**Типовые задачи:** Find Peak Element, Peak Index in a Mountain Array.

Сложность: $O(\log n)$.

## Binary search on answer

**Сигнал.** «Минимизировать максимум…», «максимизировать минимум…», «наименьшее $k$, при котором успеем/поместимся». Ответ — число из известного диапазона, и проверить конкретное значение проще, чем найти оптимум.

**Идея.** Главный фреймворк раздела. Ищем не по массиву, а по пространству ответов $[\text{lo}, \text{hi}]$. Три шага. Первый: определить диапазон — lo это минимальный осмысленный ответ (для capacity — максимальный вес одного пакета), hi — заведомо достижимый (сумма всех весов). Второй: написать функцию $\text{feasible}(x)$ — «можно ли уложиться с ответом $x$» — и убедиться, что она монотонна: если можно с $x$, то можно и с любым $x' > x$. Третий: first true по этому predicate. Оптимизационная задача превращается в серию задач-решений, а feasible-проверка — обычно жадная симуляция за $O(n)$ (пересечение с [[greedy]]).

Вариация — вещественное пространство ответов: тогда вместо `lo < hi` крутим фиксированные ~100 итераций или до $\text{hi} - \text{lo} < \varepsilon$.

```python
def min_eating_speed(piles: list[int], h: int) -> int:
    def feasible(k: int) -> bool:  # can Koko finish at speed k?
        return sum((p + k - 1) // k for p in piles) <= h

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**Типовые задачи:** Koko Eating Bananas, Capacity to Ship Packages Within D Days, Split Array Largest Sum (есть и DP-решение — [[dp-2d]]), Minimum Number of Days to Make m Bouquets, Kth Smallest Element in a Sorted Matrix (альтернатива через [[heap]]).

Сложность: $O(n \log A)$, где $A$ — размер диапазона ответов.

## Бинпоиск в 2D

**Сигнал.** Матрица $m \times n$, строки отсортированы и каждая строка начинается после конца предыдущей.

**Идея.** Такая матрица — обычный отсортированный массив длины $mn$, просто нарезанный на строки. Один бинпоиск по индексам $[0, mn)$ с пересчётом $i \mapsto (\lfloor i/n \rfloor,\ i \bmod n)$. Не путать с Search a 2D Matrix II, где строки и столбцы отсортированы независимо — там работает «лестница» из угла за $O(m + n)$, по духу ближе к [[two-pointers]].

```python
def search_matrix(matrix: list[list[int]], target: int) -> bool:
    m, n = len(matrix), len(matrix[0])
    lo, hi = 0, m * n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        val = matrix[mid // n][mid % n]  # unflatten index
        if val == target:
            return True
        if val < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False
```

**Типовые задачи:** Search a 2D Matrix.

Сложность: $O(\log mn)$.

## Partition двух массивов

**Сигнал.** Два отсортированных массива, нужна медиана или $k$-й элемент за логарифм — merge за $O(m + n)$ не проходит по требованию.

**Идея.** Ищем разрез: из массива $A$ берём в «левую часть» $i$ элементов, из $B$ — $j = \lfloor (m+n+1)/2 \rfloor - i$, так что слева ровно половина всех элементов. Разрез корректен, когда левые части не превосходят правые крест-накрест: $A[i-1] \leq B[j]$ и $B[j-1] \leq A[i]$. Бинпоиск ведём по $i$ в меньшем массиве: если $A[i-1] > B[j]$, взяли из $A$ слишком много — сдвигаемся влево, иначе вправо. Медиана собирается из четырёх граничных элементов.

```python
def find_median_sorted_arrays(a: list[int], b: list[int]) -> float:
    if len(a) > len(b):
        a, b = b, a  # binary search over the smaller array
    m, n = len(a), len(b)
    lo, hi = 0, m
    half = (m + n + 1) // 2
    while True:
        i = (lo + hi) // 2  # how many elements of a go left
        j = half - i
        a_left = a[i - 1] if i > 0 else -inf
        a_right = a[i] if i < m else inf
        b_left = b[j - 1] if j > 0 else -inf
        b_right = b[j] if j < n else inf
        if a_left <= b_right and b_left <= a_right:  # valid partition
            if (m + n) % 2:
                return float(max(a_left, b_left))
            return (max(a_left, b_left) + min(a_right, b_right)) / 2
        if a_left > b_right:
            hi = i - 1
        else:
            lo = i + 1
```

**Типовые задачи:** Median of Two Sorted Arrays.

Сложность: $O(\log \min(m, n))$.

## Bisect по таймстемпам

**Сигнал.** Версионированные данные: «верни значение ключа на момент времени $t$ или раньше».

**Идея.** Таймстемпы для каждого ключа приходят по возрастанию, так что список версий уже отсортирован — сортировать ничего не надо, только хранить. `get` — это last true по predicate $\text{ts}_i \leq t$, то есть `bisect_right - 1`. Структура — hash map из ключа в список версий, пересечение с [[arrays-hashing]].

```python
class TimeMap:
    def __init__(self):
        self.store = defaultdict(list)  # key -> [(timestamp, value)]

    def set(self, key: str, ts: int, value: str) -> None:
        self.store[key].append((ts, value))  # timestamps arrive sorted

    def get(self, key: str, ts: int) -> str:
        pairs = self.store[key]
        i = bisect_right(pairs, ts, key=lambda p: p[0]) - 1  # last ts <= t
        return pairs[i][1] if i >= 0 else ""
```

**Типовые задачи:** Time Based Key-Value Store, Snapshot Array, Online Election.

Сложность: `set` — $O(1)$, `get` — $O(\log n)$.

## Карта раздела

| Техника | Сигнал в задаче | Сложность |
| --- | --- | --- |
| Классический бинпоиск | Отсортированный массив, точный target | $O(\log n)$ |
| Граница first/last true | «Первое/последнее вхождение», позиция вставки | $O(\log n)$ |
| Rotated sorted array | «Sorted, но rotated», pivot неизвестен | $O(\log n)$ |
| Peak по «наклону» | Нужен локальный максимум, соседи задают направление | $O(\log n)$ |
| Binary search on answer | «Минимизировать максимум», «наименьшее $k$, при котором можно» | $O(n \log A)$ |
| 2D как развёрнутый массив | Матрица, строки отсортированы «встык» | $O(\log mn)$ |
| Partition двух массивов | Медиана / $k$-й элемент двух sorted массивов | $O(\log \min(m, n))$ |
| Bisect по таймстемпам | Версионированные данные, «значение на момент $t$» | $O(\log n)$ на запрос |

Та же идея живёт и в структурах данных: поиск в BST из [[trees]] — это бинпоиск, зашитый в форму дерева. А binary search on answer часто конкурирует с [[sliding-window]] и [[heap]]: если свойство окна или порогового значения монотонно, задачу можно решить любым из этих инструментов — вопрос лишь в том, какой predicate проще написать.
