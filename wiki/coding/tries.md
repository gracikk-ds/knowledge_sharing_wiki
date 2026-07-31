---
Created: 2026-07-04T11:13
Reviewed: Todo
Keywords:
  - leetcode
  - trie
  - prefix tree
  - algorithms
---
Trie (prefix tree) — дерево, где каждое ребро помечено символом, а путь от корня до узла читается как префикс. Слова с общим префиксом делят один путь, поэтому trie хранит словарь не как множество независимых строк, а как дерево общих префиксов. Каждый узел — это `children: dict[str, node]` плюс флаг `is_end`, отмечающий, что в этом узле заканчивается целое слово.

Против hash map trie выигрывает ровно тогда, когда вопрос задаётся про **префикс**, а не про целое слово: «есть ли слово, начинающееся с $p$», autocomplete, поиск по шаблону с wildcard. Hash set отвечает только на точное совпадение — префиксный запрос вырождается в перебор всего словаря. Второй выигрыш — **инкрементальный** спуск: по доске или потоку символов идём по trie шаг за шагом, и мёртвая ветка видна сразу, без пересборки строки и повторного хеширования (это сердце Word Search II). Раздел маленький, но техника всплывает в [[backtracking]], [[bit-manipulation]] и задачах на строки из [[arrays-hashing]].

## Базовый trie: insert / search / startsWith

**Сигнал.** «Реализуйте структуру данных со вставкой слов и запросами по префиксу»; много запросов вида «начинается ли что-то с $p$» к фиксированному словарю.

**Идея.** Узел — `dict` детей плюс `is_end`. Все три операции — один и тот же спуск от корня по символам: `insert` создаёт недостающие узлы по пути, `search` и `startsWith` просто проверяют, что путь существует. Разница между ними одна: `search` в конце требует `is_end` (слово целиком), `startsWith` — нет (достаточно, что путь есть). Поэтому спуск выносим в общий helper.

```python
class TrieNode:
    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True

    def find(self, prefix: str) -> TrieNode | None:
        node = self.root
        for ch in prefix:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def search(self, word: str) -> bool:
        node = self.find(word)
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        return self.find(prefix) is not None
```

**Типовые задачи:** Implement Trie (Prefix Tree), Longest Common Prefix, Search Suggestions System.

Сложность: $O(m)$ на операцию, где $m$ — длина слова; память $O(\sum m_i)$ узлов в худшем случае (без общих префиксов).

## Wildcard `.` — DFS с ветвлением

**Сигнал.** Поиск по шаблону, где спецсимвол (`.`) матчит любую букву; «add word / search word» с wildcard в запросе.

**Идея.** Обычный символ однозначно выбирает ребёнка — спуск остаётся линейным. Wildcard ломает однозначность: подходит **любой** ребёнок, поэтому в этой точке ветвимся — рекурсивный DFS по всем детям с той же оставшейся частью шаблона. Достаточно, чтобы хотя бы одна ветка дошла до конца с `is_end`. Ключевое наблюдение: платим экспонентой только за wildcard-позиции, обычные символы по-прежнему стоят $O(1)$.

```python
def search(self, word: str) -> bool:
    def dfs(i: int, node: TrieNode) -> bool:
        if i == len(word):
            return node.is_end
        ch = word[i]
        if ch == ".":
            return any(dfs(i + 1, child) for child in node.children.values())
        child = node.children.get(ch)
        return child is not None and dfs(i + 1, child)

    return dfs(0, self.root)
```

**Типовые задачи:** Design Add and Search Words Data Structure.

Сложность: $O(m)$ без wildcard; в худшем случае $O(26^k \cdot m)$, где $k$ — число точек (на практике точек 1–2, и ветки быстро умирают).

## Word Search II: trie по словарю + DFS по доске

**Сигнал.** Найти на сетке символов **много** слов из словаря сразу; наивное «запустить [[backtracking]]-поиск для каждого слова отдельно» не влезает в лимит.

**Идея.** Наивный вариант обходит доску $|W|$ раз — по разу на слово. Вместо этого строим trie по **всему словарю** и запускаем один DFS по доске, спускаясь по trie синхронно с ходом по клеткам: текущий узел trie — это «все слова словаря, начинающиеся с уже пройденного пути». Общие префиксы слов обрабатываются один раз, а не $|W|$ раз — в этом весь выигрыш. Два pruning-приёма, без которых решение всё ещё медленное: найденное слово вычёркиваем (`nxt.word = None`), а узлы, под которыми не осталось слов, физически удаляем из trie — мёртвые ветки перестают порождать рекурсию.

```python
def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    root = build_trie(words)  # word ends store node.word = full word
    rows, cols, res = len(board), len(board[0]), []

    def dfs(r: int, c: int, node: TrieNode) -> None:
        nxt = node.children.get(board[r][c])
        if nxt is None:
            return  # no dictionary word continues this way
        if nxt.word is not None:
            res.append(nxt.word)
            nxt.word = None  # report each word once
        ch, board[r][c] = board[r][c], "#"  # mark visited
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols:
                dfs(nr, nc, nxt)
        board[r][c] = ch
        if not nxt.children and nxt.word is None:
            del node.children[ch]  # prune exhausted branch

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, root)
    return res
```

**Типовые задачи:** Word Search II (Word Search I — чистый [[backtracking]] без trie, слово одно).

Сложность: построение trie — $O(\sum m_i)$; DFS в худшем случае $O(R \cdot C \cdot 4^L)$, где $L$ — длина самого длинного слова, но pruning срезает подавляющую часть веток.

## Бинарный trie по битам: максимальный XOR

**Сигнал.** «Максимизируйте $x \oplus y$ по парам из массива» — XOR-задача, где перебор пар за $O(n^2)$ не проходит.

**Идея.** Число — это строка из 32 бит, значит по числам можно построить trie с алфавитом $\{0, 1\}$. Для фиксированного $x$ лучший партнёр строится жадно от старшего бита к младшему: на каждом уровне пытаемся уйти в ветку с **противоположным** битом (она даёт единицу в старшем разряде результата, что перевешивает всё, что можно набрать младшими). Приём из [[greedy]] на структуре из этого раздела; сами битовые трюки — в [[bit-manipulation]].

```python
def find_maximum_xor(nums: list[int]) -> int:
    root: dict = {}
    for x in nums:
        node = root
        for i in range(31, -1, -1):
            node = node.setdefault(x >> i & 1, {})
    best = 0
    for x in nums:
        node, cur = root, 0
        for i in range(31, -1, -1):
            b = x >> i & 1
            if 1 - b in node:  # opposite bit maximizes this position
                cur |= 1 << i
                node = node[1 - b]
            else:
                node = node[b]
        best = max(best, cur)
    return best
```

**Типовые задачи:** Maximum XOR of Two Numbers in an Array, Maximum XOR With an Element From Array.

Сложность: $O(32 \cdot n)$ по времени и памяти.

## Trie vs hash map / hash set

**Сигнал.** Это не техника, а развилка на собеседовании: «а почему не hash set?». Ответ должен быть готов до того, как мы начали писать trie.

**Идея.** На точных запросах hash set не хуже и проще — trie не даёт ничего, кроме overhead-а на узлы. Trie окупается, когда запрос про префикс, шаблон или когда нужен инкрементальный спуск символ за символом. Память — палка о двух концах: общие префиксы trie хранит один раз, но каждый узел — это отдельный объект со своим `dict`.

| Операция | Hash set | Trie |
|---|---|---|
| Точный поиск / вставка слова | $O(m)$ (хеш строки) | $O(m)$ |
| «Есть ли слово с префиксом $p$» | $O(n \cdot m)$ — перебор словаря | $O(\vert p \vert)$ |
| Все слова с префиксом (autocomplete) | $O(n \cdot m)$ | $O(\vert p \vert + \text{выдача})$ |
| Поиск с wildcard `.` | перебор словаря | DFS от точки ветвления |
| Инкрементальный спуск по символу | нет (пересобираем строку) | $O(1)$ за шаг |
| Память | по слову на запись | общие префиксы — один раз, но overhead на узлы |

**Типовые задачи:** развилка всплывает в Word Search II (без trie — TLE) и Search Suggestions System (там хватает сортировки + [[binary-search]]).

## Карта раздела

| Техника | Сигнал в задаче | Сложность |
|---|---|---|
| Базовый trie | Словарь + запросы по префиксу, «implement trie» | $O(m)$ на операцию |
| Wildcard DFS | Шаблон с `.` — ветвимся по всем детям | $O(m)$ … $O(26^k \cdot m)$ |
| Trie + DFS по доске | Много слов на одной сетке → [[backtracking]] | $O(R \cdot C \cdot 4^L)$ c pruning |
| Бинарный trie | Максимизация XOR по парам → [[bit-manipulation]] | $O(32 \cdot n)$ |
| Trie vs hash set | Префикс/шаблон → trie; точный поиск → hash set | — |
