---
Created: 2026-07-04T11:13
Reviewed: Todo
Keywords:
  - leetcode
  - backtracking
  - algorithms
---
Backtracking — систематический перебор всех кандидатов через рекурсию с откатом: на каждом узле дерева решений мы делаем выбор (**choose**), рекурсивно исследуем последствия (**explore**) и отменяем выбор, возвращая состояние как было (**unchoose**). По сути это DFS по неявному дереву решений, где путь от корня до узла — частично построенный ответ.

Сигналы, что мы в этом разделе: «верните **все** варианты», «все комбинации/перестановки/разбиения», расстановка на доске, набор ограничений, которые надо удовлетворить. Сложность почти всегда экспоненциальная — дерево ветвится в каждом узле, и число листьев растёт как $2^n$, $n!$ или $k^n$; наша задача не победить экспоненту (ответов и правда столько), а не делать лишней работы — за это отвечает pruning. Если же нужен не список всех ответов, а только их количество или «можно/нельзя», и состояние зависит лишь от «остатка» задачи — перебор схлопывается мемоизацией в DP ([[dp-1d]]).

## Общий шаблон: choose → explore → unchoose

**Сигнал.** Любая задача на «перечислить все решения»; остальные техники раздела — специализации этого шаблона.

**Идея.** Держим мутируемый `path` — текущую ветку дерева — и общий список `res`. В каждом узле перебираем допустимые выборы: добавляем выбор в `path`, рекурсивно спускаемся, убираем обратно. Ключевая деталь — при записи ответа кладём **копию** `path[:]`: сам `path` продолжит мутировать, и без копии в `res` окажутся ссылки на один и тот же (в итоге пустой) список.

```python
def backtrack(state) -> None:
    if is_solution(state):
        res.append(path[:])  # copy! path keeps mutating after return
        return
    for choice in candidates(state):
        path.append(choice)    # choose
        backtrack(new_state)   # explore
        path.pop()             # unchoose
```

**Типовые задачи:** весь раздел ниже.

Сложность: $O(\text{число листьев} \cdot \text{стоимость копии})$, как правило экспоненциальная.

## Subsets: включить/не включить vs цикл по start

**Сигнал.** «Все подмножества», power set; порядок внутри подмножества не важен.

**Идея.** Два эквивалентных стиля. Первый — бинарное решение по каждому элементу: «взять $\text{nums}[i]$ или пропустить», дерево — полное бинарное глубины $n$ с $2^n$ листьями. Второй — цикл `for i in range(start, n)` с рекурсией от $i+1$: каждый **узел** дерева (не только лист) — готовое подмножество, поэтому `res.append` стоит в начале функции. Второй стиль удобнее для дубликатов: после сортировки одинаковые элементы стоят рядом, и повтор **на одном уровне дерева** (`i > start`) порождает уже перебранную ветку — пропускаем.

```python
def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    nums.sort()  # needed only for the duplicate skip
    res, path = [], []
    def backtrack(start: int) -> None:
        res.append(path[:])  # every node is a valid subset
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue  # same value on the same level -> duplicate branch
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()
    backtrack(0)
    return res
```

**Типовые задачи:** Subsets, Subsets II, Letter Case Permutation.

Сложность: $O(n \cdot 2^n)$ — подмножеств $2^n$, копия каждого стоит до $O(n)$.

## Combination Sum: повторы разрешены vs запрещены

**Сигнал.** «Все комбинации с суммой target»; вопрос номер один — можно ли брать один элемент несколько раз.

**Идея.** Отличие от subsets — в том, куда двигается `start` при спуске. Повторное использование разрешено — рекурсируем с тем же $i$ (элемент может выбрать сам себя снова); запрещено — с $i+1$. Дубликаты в ответе (Combination Sum II) убираются тем же пропуском на уровне, что и в Subsets II. Обязательное отсечение: сортируем кандидатов и выходим из цикла, как только кандидат превысил остаток суммы — все следующие ещё больше.

```python
def combination_sum(cands: list[int], target: int) -> list[list[int]]:
    cands.sort()
    res, path = [], []
    def backtrack(start: int, remain: int) -> None:
        if remain == 0:
            res.append(path[:])
            return
        for i in range(start, len(cands)):
            if cands[i] > remain:
                break  # sorted: all further candidates are too large
            path.append(cands[i])
            backtrack(i, remain - cands[i])  # i (reuse) vs i + 1 (no reuse)
            path.pop()
    backtrack(0, target)
    return res
```

**Типовые задачи:** Combination Sum, Combination Sum II, Combinations.

Сложность: экспоненциальная — грубая оценка $O(2^{t/m})$, где $t$ — target, $m$ — минимальный кандидат (глубина дерева ограничена $t/m$).

## Permutations: used-массив или swap

**Сигнал.** «Все перестановки» — порядок важен, каждый элемент используется ровно один раз.

**Идея.** Выбор — какой элемент поставить на текущую позицию, поэтому цикл каждый раз идёт по **всем** элементам, а занятые отмечаем в `used`. Альтернатива без доппамяти — swap-подход: на позиции $k$ меняем местами $\text{nums}[k]$ с каждым из $\text{nums}[k..n-1]$, рекурсируем, свапаем обратно. Для дубликатов (Permutations II) после сортировки пропускаем $\text{nums}[i] = \text{nums}[i-1]$, если левый близнец ещё не использован: иначе две одинаковые ветки строят одну и ту же перестановку.

```python
def permute_unique(nums: list[int]) -> list[list[int]]:
    nums.sort()
    res, path = [], []
    used = [False] * len(nums)
    def backtrack() -> None:
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i, x in enumerate(nums):
            if used[i] or (i > 0 and nums[i] == nums[i - 1] and not used[i - 1]):
                continue
            used[i] = True
            path.append(x)
            backtrack()
            path.pop()
            used[i] = False
    backtrack()
    return res
```

**Типовые задачи:** Permutations, Permutations II.

Сложность: $O(n \cdot n!)$ — перестановок $n!$, каждая копируется за $O(n)$.

## Строковые разбиения

**Сигнал.** Разрезать строку на куски с условием на каждый кусок; или каждой позиции сопоставить один из нескольких символов.

**Идея.** Выбор — «где заканчивается следующий кусок»: перебираем все префиксы от `start`, валидные (палиндром, корректный октет IP) продлевают ветку, рекурсия идёт с конца куска. Между любыми соседними символами либо стоит разрез, либо нет — отсюда $2^{n-1}$ вариантов разбиения. Letter Combinations of a Phone Number — вырожденный случай без отката состояния: на каждую цифру 3–4 буквы, дерево ширины 4 и глубины $n$. Если нужен не список разбиений, а «можно ли разрезать» или их число — это Word Break, то есть [[dp-1d]].

```python
def partition(s: str) -> list[list[str]]:
    res, path = [], []
    def backtrack(start: int) -> None:
        if start == len(s):
            res.append(path[:])
            return
        for end in range(start + 1, len(s) + 1):
            prefix = s[start:end]
            if prefix == prefix[::-1]:  # cut here only if prefix is valid
                path.append(prefix)
                backtrack(end)
                path.pop()
    backtrack(0)
    return res
```

**Типовые задачи:** Palindrome Partitioning, Letter Combinations of a Phone Number, Restore IP Addresses.

Сложность: $O(n \cdot 2^n)$ для разбиений; $O(n \cdot 4^n)$ для phone number.

## Поиск на доске: Word Search

**Сигнал.** 2D-сетка, путь из соседних клеток, «есть ли слово/маршрут». По сути DFS по неявному графу — родня [[graphs]].

**Идея.** Запускаем DFS из каждой клетки. Состояние здесь — сама доска: вместо отдельного `visited` временно затираем клетку маркером (choose) и восстанавливаем при откате (unchoose), чтобы путь не наступал сам на себя. Когда слов много (Word Search II), по одной ветке DFS проверяем сразу все слова через trie и обрезаем ветку, как только префикса нет в дереве, — разбор в [[tries]].

```python
def exist(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])
    def dfs(r: int, c: int, i: int) -> bool:
        if i == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[i]:
            return False
        board[r][c] = "#"  # choose: mark cell as visited
        found = any(dfs(r + dr, c + dc, i + 1)
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        board[r][c] = word[i]  # unchoose: restore the cell
        return found
    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
```

**Типовые задачи:** Word Search, Word Search II ([[tries]]).

Сложность: $O(m \cdot n \cdot 3^L)$, где $L$ — длина слова: из каждой клетки не более трёх направлений вперёд (назад не возвращаемся).

## Constraint satisfaction: N-Queens

**Сигнал.** Расставить объекты так, чтобы выполнялся набор взаимных ограничений; «все валидные конфигурации».

**Идея.** Сужаем пространство выбора структурой задачи: в каждой строке ровно одна queen, значит рекурсия идёт по строкам, а выбор — колонка. Ограничения храним множествами занятых колонок и диагоналей: у диагонали $\nearrow$ константа $r + c$, у диагонали $\searrow$ — $r - c$, проверка выбора за $O(1)$. Choose — добавить в три множества, unchoose — убрать. Sudoku Solver — тот же паттерн с множествами по строкам/колонкам/боксам.

```python
def total_n_queens(n: int) -> int:
    cols, diag, anti = set(), set(), set()
    def backtrack(r: int) -> int:
        if r == n:
            return 1
        count = 0
        for c in range(n):
            if c in cols or (r - c) in diag or (r + c) in anti:
                continue
            cols.add(c); diag.add(r - c); anti.add(r + c)      # choose
            count += backtrack(r + 1)                          # explore
            cols.remove(c); diag.remove(r - c); anti.remove(r + c)  # unchoose
        return count
    return backtrack(0)
```

**Типовые задачи:** N-Queens, N-Queens II, Sudoku Solver.

Сложность: $O(n!)$ — в первой строке $n$ вариантов, дальше ограничения быстро режут ветвление.

## Pruning: как не делать лишней работы

Экспоненту не убрать, но константу и целые поддеревья — можно. Рабочий набор: **сортировка + ранний `break`** (как в Combination Sum — дальше только элементы крупнее остатка); **пропуск дубликатов на одном уровне** после сортировки (Subsets II, Permutations II); **feasibility-check** — если элементов осталось меньше, чем нужно добрать, ветку можно не открывать (в Combinations это срезает почти половину дерева); **симметрии** — в N-Queens достаточно перебрать первую queen в левой половине доски и удвоить ответ. Отдельный случай: если `path` не важен, а важно только агрегированное состояние (остаток суммы, позиция в строке), повторяющиеся поддеревья мемоизируются — и перебор превращается в [[dp-1d]] / [[dp-2d]].

## Карта раздела

| Техника | Сигнал в задаче | Сложность |
|---|---|---|
| Общий шаблон choose/explore/unchoose | «Верните все решения» | экспоненциальная |
| Subsets (include/exclude или start) | Все подмножества, power set | $O(n \cdot 2^n)$ |
| Combination Sum ($i$ vs $i+1$) | Комбинации с суммой; повторы да/нет | $O(2^{t/m})$ |
| Permutations (used или swap) | Все перестановки, порядок важен | $O(n \cdot n!)$ |
| Строковые разбиения | Разрезы строки с условием на кусок | $O(n \cdot 2^n)$ |
| Поиск на доске | Путь по соседним клеткам сетки → [[graphs]], [[tries]] | $O(m \cdot n \cdot 3^L)$ |
| Constraint satisfaction | Расстановка с взаимными ограничениями | $O(n!)$ |
| Pruning | Сортировка + break, дубликаты, симметрии | режет константу и поддеревья |
