---
Created: 2026-07-04T11:12
Reviewed: Todo
Keywords:
  - leetcode
  - neetcode
  - sliding window
  - algorithms
---
Sliding window — класс задач про **contiguous** subarray или substring: найти самый длинный/короткий отрезок с нужным свойством или посчитать число таких отрезков. Ключевое слово «contiguous» — если подпоследовательность можно рвать, это уже не наш раздел, а скорее [[dp-1d]]. Технически sliding window — частный случай [[two-pointers]]: оба указателя движутся в одну сторону и никогда не откатываются, поэтому суммарно каждый проходит массив один раз и получается $O(n)$ вместо наивных $O(n^2)$ проверок всех отрезков.

Сигналы, что задача отсюда: «longest/shortest substring such that…», «maximum sum of subarray of size $k$», «count subarrays with…», плюс ограничение на **содержимое окна** (не больше $k$ различных символов, сумма меньше цели, не больше $k$ замен). Ограничение должно быть **монотонным**: если окно валидно, то и любое его под-окно валидно (или наоборот) — именно это позволяет двигать границы жадно, не откатываясь.

## Фиксированное окно

**Сигнал.** Размер окна $k$ задан в условии явно: «subarray of size $k$», «average of $k$ elements».

**Идея.** Не пересчитываем агрегат окна заново, а обновляем инкрементально: сдвинули окно на шаг — добавили правый элемент, убрали левый. Один проход, каждый элемент входит и выходит из окна ровно по разу.

```python
def find_max_average(nums: list[int], k: int) -> float:
    window_sum = sum(nums[:k])
    best = window_sum
    for r in range(k, len(nums)):
        window_sum += nums[r] - nums[r - k]  # slide: add right, drop left
        best = max(best, window_sum)
    return best / k
```

Best Time to Buy and Sell Stock — тот же однопроходный паттерн, только «окно» растягивается влево неограниченно: держим минимум цены слева и на каждом шаге сравниваем `price - min_so_far` с ответом.

**Типовые задачи:** Maximum Average Subarray I, Best Time to Buy and Sell Stock, Contains Duplicate II.

Сложность: $O(n)$ по времени, $O(1)$ по памяти.

## Переменное окно: расширяем правым, сжимаем левым

**Сигнал.** «Longest substring/subarray such that…» + монотонное ограничение на содержимое (нет повторов, сумма $\leq$ цели, не более $k$ различных элементов). Главный шаблон раздела.

**Идея.** Правый указатель всегда идёт вперёд и расширяет окно. Как только invariant нарушен — двигаем левый, пока валидность не восстановится. Откатывать окно не нужно: если отрезок $[l, r]$ невалиден, то невалидно и любое его расширение вправо, поэтому все окна с этим левым краем уже бесперспективны и $l$ можно двигать только вперёд. Каждый указатель проходит массив один раз — амортизированно $O(n)$.

```python
def length_of_longest_substring(s: str) -> int:
    seen: set[str] = set()
    left = best = 0
    for right, ch in enumerate(s):
        while ch in seen:            # invariant violated -> shrink
            seen.remove(s[left])
            left += 1
        seen.add(ch)
        best = max(best, right - left + 1)
    return best
```

**Типовые задачи:** Longest Substring Without Repeating Characters, Minimum Size Subarray Sum, Max Consecutive Ones III, Fruit Into Basket.

Сложность: $O(n)$ по времени, $O(\min(n, |\Sigma|))$ по памяти на множество/счётчик.

## Окно + счётчики частот

**Сигнал.** Ищем anagram/permutation одной строки внутри другой: окно фиксированной длины, но валидность определяется **совпадением частот** символов.

**Идея.** Держим два счётчика — `need` для паттерна и `window` для текущего окна — и сдвигаем окно как фиксированное. Наивное сравнение счётчиков на каждом шаге стоит $O(|\Sigma|)$; трюк — держать число `matched` символов, у которых частоты уже совпали, и обновлять его в $O(1)$ при каждом входе/выходе символа: окно валидно, когда `matched == 26`.

```python
from collections import Counter

def find_anagrams(s: str, p: str) -> list[int]:
    k, need = len(p), Counter(p)
    if k > len(s):
        return []
    window = Counter(s[:k])
    res = [0] if window == need else []
    for r in range(k, len(s)):
        window[s[r]] += 1
        window[s[r - k]] -= 1
        if window[s[r - k]] == 0:
            del window[s[r - k]]     # keep counters comparable
        if window == need:
            res.append(r - k + 1)
    return res
```

Счётчики — это те же hash map из [[arrays-hashing]], только с инкрементальным обновлением.

**Типовые задачи:** Permutation in String, Find All Anagrams in a String.

Сложность: $O(n \cdot |\Sigma|)$ с прямым сравнением счётчиков, $O(n)$ с трюком `matched`; память $O(|\Sigma|)$.

## Окно с бюджетом замен

**Сигнал.** «Longest substring, если можно заменить не более $k$ символов» — валидность окна выражается через его самый частый элемент.

**Идея.** Окно валидно, пока $\text{window\_len} - \text{max\_freq} \leq k$: всё, что не самый частый символ, заменяем, и на это должно хватить бюджета. Тонкость: `max_freq` можно **не уменьшать** при сжатии. Ответ растёт только когда `max_freq` растёт, поэтому завышенный (устаревший) `max_freq` лишь замораживает размер окна на историческом максимуме — невалидного ответа он дать не может. Окно никогда не сжимается ниже лучшего найденного, и ответ — его финальная длина.

```python
from collections import Counter

def character_replacement(s: str, k: int) -> int:
    count: Counter[str] = Counter()
    left = max_freq = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        max_freq = max(max_freq, count[ch])
        if right - left + 1 - max_freq > k:  # budget exceeded
            count[s[left]] -= 1
            left += 1                        # shift, never shrink below best
    return len(s) - left
```

**Типовые задачи:** Longest Repeating Character Replacement, Max Consecutive Ones III.

Сложность: $O(n)$ по времени, $O(|\Sigma|)$ по памяти.

## Minimum Window Substring: сжатие для минимума

**Сигнал.** Ищем **кратчайшее** окно, покрывающее требование (все символы строки $t$ с учётом кратности). Логика зеркальна главному шаблону: расширяем до валидности, потом жадно сжимаем, пока валидность не сломается, — минимум лежит на границе.

**Идея.** Счётчик `need` фиксирует требования, `have` — число символов, по которым требование уже выполнено (с учётом кратности). Расширяем правым краем до `have == required`, затем сжимаем левым, снимая ответ на каждом шаге: как только выкинули нужный символ ниже нормы — окно снова невалидно, возвращаемся к расширению.

```python
from collections import Counter

def min_window(s: str, t: str) -> str:
    need, window = Counter(t), Counter()
    have, required = 0, len(need)
    best, left = (float("inf"), 0, 0), 0
    for right, ch in enumerate(s):
        window[ch] += 1
        if window[ch] == need[ch]:
            have += 1
        while have == required:              # valid -> shrink for minimum
            if right - left + 1 < best[0]:
                best = (right - left + 1, left, right)
            window[s[left]] -= 1
            if window[s[left]] < need[s[left]]:
                have -= 1
            left += 1
    length, l, r = best
    return "" if length == float("inf") else s[l : r + 1]
```

**Типовые задачи:** Minimum Window Substring, Minimum Size Subarray Sum.

Сложность: $O(n + m)$ по времени, $O(|\Sigma|)$ по памяти.

## Monotonic deque: max/min в окне

**Сигнал.** Нужен максимум (или минимум) в каждом окне размера $k$ — агрегат, который не обновляется инкрементально: при выходе максимума из окна непонятно, кто следующий.

**Идея.** Держим deque индексов с убывающими значениями — это monotonic stack из [[stack]], у которого дополнительно выбрасывается устаревшая голова. Перед добавлением нового элемента выкидываем с хвоста всех, кто меньше: они моложе и слабее, максимумом уже не станут никогда. Голова deque — всегда текущий максимум. Каждый элемент входит и выходит из deque по разу — амортизированно $O(n)$.

```python
from collections import deque

def max_sliding_window(nums: list[int], k: int) -> list[int]:
    dq: deque[int] = deque()   # indices, values strictly decreasing
    res = []
    for r, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()           # younger and smaller -> never the max
        dq.append(r)
        if dq[0] == r - k:
            dq.popleft()       # left edge fell out of the window
        if r >= k - 1:
            res.append(nums[dq[0]])
    return res
```

**Типовые задачи:** Sliding Window Maximum, Shortest Subarray with Sum at Least K (deque по prefix sums).

Сложность: $O(n)$ по времени, $O(k)$ по памяти.

## Подсчёт: exactly K = atMost(K) − atMost(K−1)

**Сигнал.** «Count subarrays with **exactly** $k$…» — условие «ровно $k$» не монотонно (под-окно валидного окна может стать невалидным), и напрямую окно не работает.

**Идея.** Сводим к монотонному: «не более $k$» уже решается обычным переменным окном, а число subarray с ровно $k$ — это разность $\text{atMost}(k) - \text{atMost}(k-1)$. Внутри `at_most` ключевая строка — `res += right - left + 1`: для каждого правого края все `right - left + 1` отрезков, заканчивающихся в нём, валидны, потому что окно максимально растянуто влево.

```python
from collections import Counter

def subarrays_with_k_distinct(nums: list[int], k: int) -> int:
    def at_most(k: int) -> int:
        count: Counter[int] = Counter()
        left = res = 0
        for right, x in enumerate(nums):
            count[x] += 1
            while len(count) > k:
                count[nums[left]] -= 1
                if count[nums[left]] == 0:
                    del count[nums[left]]
                left += 1
            res += right - left + 1  # windows ending at right
        return res

    return at_most(k) - at_most(k - 1)
```

**Типовые задачи:** Subarrays with K Different Integers, Count Number of Nice Subarrays, Binary Subarrays With Sum.

Сложность: $O(n)$ по времени (два прохода), $O(k)$ по памяти.

## Карта раздела

| Техника | Сигнал в задаче | Сложность |
| --- | --- | --- |
| Фиксированное окно | Размер окна $k$ задан явно | $O(n)$ |
| Переменное окно (расширяем/сжимаем) | Longest + монотонное ограничение на содержимое | $O(n)$ |
| Окно + счётчики частот | Anagram/permutation внутри строки | $O(n)$ |
| Окно с бюджетом замен | Longest при $\leq k$ заменах | $O(n)$ |
| Сжатие для минимума (have/need) | Shortest окно, покрывающее требование | $O(n + m)$ |
| Monotonic deque | Max/min в каждом окне | $O(n)$ |
| atMost(K) − atMost(K−1) | Count subarrays с «ровно $k$» | $O(n)$ |
