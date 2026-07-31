---
Created: 2026-07-04T11:15
Reviewed: Todo
Keywords:
  - leetcode
  - neetcode
  - dynamic programming
  - algorithms
---
Dynamic programming — это рекурсия по подзадачам, у которой есть два свойства: **перекрывающиеся подзадачи** (одна и та же подзадача возникает много раз, поэтому её ответ стоит закэшировать) и **оптимальная подструктура** (оптимальный ответ большой задачи собирается из оптимальных ответов подзадач). Если хотя бы одного свойства нет — это не DP: без перекрытия достаточно обычной рекурсии, без оптимальной подструктуры кэш ничего не даёт.

Сигналы, что задача отсюда: «сколькими способами…», «минимальная/максимальная стоимость…», «можно ли достичь/составить…» — и при этом жадный локальный выбор ломается на контрпримерах (иначе это [[greedy]]), а перебор всех вариантов экспоненциален. Главный вопрос при разработке решения: **что является состоянием и каким был последний выбор**. Ответ на него и есть рекуррентное соотношение: состояние — аргумент $dp$, перебор последнего выбора — правая часть.

Рабочий процесс всегда один: brute force рекурсия → memoization (top-down) → таблица (bottom-up) → оптимизация памяти. Мемоизированный [[backtracking]] — это буквально и есть top-down DP, отдельно его учить не нужно. Bottom-up — та же рекурсия, развёрнутая в цикл по возрастанию состояния. А если $dp[i]$ зависит только от фиксированного числа предыдущих значений, таблица сжимается до пары переменных — память $O(1)$. Здесь состояние одномерное; как только его приходится расширять до пары индексов — это [[dp-2d]].

## Fibonacci-паттерн

**Сигнал.** Ответ для $i$ собирается из ответов для фиксированного числа предыдущих позиций: «на сколько ступенек можно шагнуть», «из каких соседних позиций сюда приходим».

**Состояние и переход.** $dp[i]$ — ответ для префикса длины $i$ (число способов добраться до ступеньки $i$, минимальная стоимость до неё).

$$
dp[i] = dp[i-1] + dp[i-2]
$$

Зависимость только от двух последних значений — храним две переменные вместо массива.

```python
def climb_stairs(n: int) -> int:
    prev, cur = 1, 1  # dp[0], dp[1]
    for _ in range(2, n + 1):
        prev, cur = cur, prev + cur
    return cur
```

**Типовые задачи:** Climbing Stairs, Min Cost Climbing Stairs, N-th Tribonacci Number.

Сложность: $O(n)$ по времени, $O(1)$ по памяти.

## Take / skip

**Сигнал.** На каждой позиции бинарный выбор «взять или пропустить», причём взятие блокирует соседа.

**Состояние и переход.** $dp[i]$ — максимум добычи на префиксе до дома $i$. Последний выбор: либо дом $i$ пропустили, либо взяли — тогда $i-1$ брать было нельзя.

$$
dp[i] = \max\big(dp[i-1],\ dp[i-2] + \text{nums}[i]\big)
$$

```python
def rob(nums: list[int]) -> int:
    prev, cur = 0, 0
    for x in nums:
        prev, cur = cur, max(cur, prev + x)
    return cur
```

House Robber II (дома по кольцу): первый и последний дом — соседи, поэтому вместе их не взять. Трюк — два прогона обычного `rob`: по `nums[1:]` и по `nums[:-1]`, ответ — максимум из двух.

**Типовые задачи:** House Robber, House Robber II, Delete and Earn.

Сложность: $O(n)$ по времени, $O(1)$ по памяти.

## Подсчёт способов с ветвлением по валидности

**Сигнал.** «Сколькими способами можно разбить/декодировать строку», где на каждом шаге откусываем один или два символа, но не всякий кусок валиден.

**Состояние и переход.** $dp[i]$ — число способов декодировать префикс длины $i$. Тот же Fibonacci-паттерн, только каждая ветка входит в сумму с условием (нулевой символ сам по себе не декодируется, пара валидна только в диапазоне $10..26$):

$$
dp[i] = [\,s_i \neq 0\,] \cdot dp[i-1] + [\,10 \leq \overline{s_{i-1} s_i} \leq 26\,] \cdot dp[i-2]
$$

```python
def num_decodings(s: str) -> int:
    if s[0] == "0":
        return 0
    prev2, prev1 = 1, 1  # dp for empty prefix and first char
    for i in range(1, len(s)):
        cur = 0
        if s[i] != "0":
            cur += prev1
        if "10" <= s[i - 1 : i + 1] <= "26":
            cur += prev2
        prev2, prev1 = prev1, cur
    return prev1
```

**Типовые задачи:** Decode Ways, Fibonacci-задачи с ограничениями на шаг.

Сложность: $O(n)$ по времени, $O(1)$ по памяти.

## Unbounded knapsack в 1D

**Сигнал.** Набираем целевую сумму из предметов, каждый предмет можно брать **неограниченно**: монеты, комбинации слагаемых.

**Состояние и переход.** $dp[a]$ — минимум монет, чтобы набрать сумму $a$. Последний выбор — какая монета легла последней:

$$
dp[a] = 1 + \min_{c \in \text{coins},\ c \leq a} dp[a - c]
$$

```python
def coin_change(coins: list[int], amount: int) -> int:
    dp = [0] + [float("inf")] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] != float("inf") else -1
```

Coin Change II (число **комбинаций**, а не минимум) — тот же массив, но внешний цикл по монетам, а не по суммам, чтобы не считать перестановки одной комбинации отдельно; концептуально это сплющенная таблица «монета $\times$ сумма» из [[dp-2d]].

**Типовые задачи:** Coin Change, Coin Change II, Perfect Squares, Combination Sum IV.

Сложность: $O(n \cdot |\text{coins}|)$ по времени, $O(n)$ по памяти.

## Подмножества как 0/1 knapsack по сумме

**Сигнал.** «Можно ли выбрать подмножество с суммой $t$», каждый элемент используется **не больше одного раза**.

**Состояние и переход.** $dp[s]$ — достижима ли сумма $s$ из уже рассмотренных элементов. Новый элемент $x$ расширяет множество достижимых сумм:

$$
dp[s] = dp[s] \ \lor\ dp[s - x]
$$

Ключевой трюк — обход суммы **справа налево**: тогда $dp[s-x]$ ещё не обновлён текущим элементом, и $x$ не может быть взят дважды. Слева направо получился бы unbounded-вариант из предыдущего раздела — вся разница между 0/1 и unbounded knapsack в 1D сидит в направлении цикла.

```python
def can_partition(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    dp = [True] + [False] * target
    for x in nums:
        for s in range(target, x - 1, -1):  # right to left: each x used once
            dp[s] = dp[s] or dp[s - x]
    return dp[target]
```

**Типовые задачи:** Partition Equal Subset Sum, Target Sum, Last Stone Weight II.

Сложность: $O(n \cdot t)$ по времени, $O(t)$ по памяти, где $t$ — целевая сумма.

## Longest Increasing Subsequence

**Сигнал.** Самая длинная подпоследовательность (можно рвать, порядок сохраняется) с условием возрастания или сравнимости соседей.

**Состояние и переход.** $dp[i]$ — длина самой длинной возрастающей подпоследовательности, **заканчивающейся ровно в** $i$. Последний выбор — какой элемент стоял перед $\text{nums}[i]$:

$$
dp[i] = 1 + \max_{j < i,\ \text{nums}[j] < \text{nums}[i]} dp[j]
$$

Это $O(n^2)$. Ускорение до $O(n \log n)$ — patience sorting: держим `tails`, где `tails[k]` — минимальный хвост возрастающей подпоследовательности длины $k+1$. Массив `tails` отсортирован, поэтому позицию нового элемента ищем через `bisect_left` — см. [[binary-search]].

```python
from bisect import bisect_left

def length_of_lis(nums: list[int]) -> int:
    tails: list[int] = []  # tails[k] = min tail of increasing subseq of len k+1
    for x in nums:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)
```

**Типовые задачи:** Longest Increasing Subsequence, Number of LIS, Russian Doll Envelopes (сортировка + LIS).

Сложность: $O(n^2)$ таблицей, $O(n \log n)$ через patience sorting.

## Word Break: dp по префиксам

**Сигнал.** «Можно ли разрезать строку на куски из словаря» — состояние живёт на границах между символами.

**Состояние и переход.** $dp[i]$ — можно ли разбить префикс $s[:i]$. Последний выбор — где начинается последнее слово:

$$
dp[i] = \bigvee_{j < i} \Big( dp[j] \wedge s[j{:}i] \in \text{dict} \Big)
$$

```python
def word_break(s: str, word_dict: list[str]) -> bool:
    words = set(word_dict)  # O(1) lookup
    dp = [True] + [False] * len(s)  # dp[i]: prefix s[:i] is breakable
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    return dp[-1]
```

Словарь обязательно кладём в `set`; внутренний цикл можно ограничить длиной самого длинного слова. Перечислить **все** разбиения (Word Break II) — уже мемоизированный [[backtracking]].

**Типовые задачи:** Word Break, Word Break II, Palindrome Partitioning (та же схема, predicate — «кусок — палиндром»).

Сложность: $O(n^2)$ по времени (плюс срезы), $O(n)$ по памяти.

## Два состояния из-за знака

**Сигнал.** Максимизируем произведение или другую величину, где «плохое» значение (большой минус) одним умножением превращается в «хорошее».

**Состояние и переход.** Одного $dp[i]$ мало: минимум тоже нужно тащить, потому что отрицательный элемент меняет минимум и максимум местами. Держим пару — $\text{mx}[i]$ и $\text{mn}[i]$, максимальное и минимальное произведение subarray, заканчивающегося в $i$:

$$
\begin{aligned}
\text{mx}[i] &= \max\big(x_i,\ x_i \cdot \text{mx}[i-1],\ x_i \cdot \text{mn}[i-1]\big) \\
\text{mn}[i] &= \min\big(x_i,\ x_i \cdot \text{mx}[i-1],\ x_i \cdot \text{mn}[i-1]\big)
\end{aligned}
$$

Это Kadane (Maximum Subarray) с удвоенным состоянием — общий приём: если переход зависит от чего-то ещё (знак, «держим ли акцию», использован ли джокер), это «что-то» добавляется в состояние.

```python
def max_product(nums: list[int]) -> int:
    best = mx = mn = nums[0]
    for x in nums[1:]:
        candidates = (x, x * mx, x * mn)
        mx, mn = max(candidates), min(candidates)
        best = max(best, mx)
    return best
```

**Типовые задачи:** Maximum Product Subarray, Maximum Subarray (одно состояние — вырожденный случай), Best Time to Buy and Sell Stock with Cooldown (состояния «держим/не держим»).

Сложность: $O(n)$ по времени, $O(1)$ по памяти.

## Палиндромы: expand around center vs таблица

**Сигнал.** Найти или посчитать палиндромные substrings.

**Состояние и переход.** Табличный вариант: $dp[i][j]$ — является ли $s[i..j]$ палиндромом; палиндром — это равные концы вокруг палиндрома-ядра:

$$
dp[i][j] = (s_i = s_j) \wedge dp[i+1][j-1]
$$

Состояние двумерное — формально это [[dp-2d]], и таблица нужна, когда ответы $dp[i][j]$ переиспользуются другой DP (Palindromic Substring Partitioning). Для самих Longest Palindromic Substring и Palindromic Substrings проще **expand around center**: у палиндрома $2n-1$ возможных центров (символ или пара), из каждого расширяемся, пока концы совпадают. Та же $O(n^2)$ по времени, но $O(1)$ памяти и без возни с порядком заполнения таблицы.

```python
def count_substrings(s: str) -> int:
    def expand(l: int, r: int) -> int:
        count = 0
        while l >= 0 and r < len(s) and s[l] == s[r]:
            count += 1
            l, r = l - 1, r + 1
        return count

    return sum(expand(i, i) + expand(i, i + 1) for i in range(len(s)))
```

**Типовые задачи:** Longest Palindromic Substring, Palindromic Substrings.

Сложность: $O(n^2)$ по времени; $O(1)$ по памяти у expand around center против $O(n^2)$ у таблицы.

## Карта раздела

| Паттерн | Состояние | Типовая задача | Сложность |
| --- | --- | --- | --- |
| Fibonacci | $dp[i]$ — ответ для префикса $i$, зависит от $k$ последних | Climbing Stairs | $O(n)$, память $O(1)$ |
| Take / skip | $dp[i]$ — максимум на префиксе, взяли или пропустили $i$ | House Robber | $O(n)$, память $O(1)$ |
| Ветвление по валидности | $dp[i]$ — число способов декодировать префикс | Decode Ways | $O(n)$, память $O(1)$ |
| Unbounded knapsack | $dp[a]$ — минимум предметов на сумму $a$ | Coin Change | $O(n \cdot k)$ |
| 0/1 knapsack по сумме | $dp[s]$ — достижима ли сумма $s$; обход справа налево | Partition Equal Subset Sum | $O(n \cdot t)$ |
| LIS | $dp[i]$ — длина LIS, заканчивающейся в $i$ | Longest Increasing Subsequence | $O(n^2)$ или $O(n \log n)$ |
| DP по префиксам | $dp[i]$ — разбиваем ли префикс $s[:i]$ | Word Break | $O(n^2)$ |
| Два состояния (знак) | пара $(\text{mx}[i], \text{mn}[i])$ | Maximum Product Subarray | $O(n)$, память $O(1)$ |
| Палиндромы | центр расширения или $dp[i][j]$ (→ [[dp-2d]]) | Longest Palindromic Substring | $O(n^2)$ |
