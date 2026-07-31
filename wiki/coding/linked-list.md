---
Created: 2026-07-04T11:13
Reviewed: Todo
Keywords:
  - leetcode
  - linked list
  - fast and slow pointers
---
Linked List на Neetcode — это класс задач, где структура данных не даёт random access: чтобы попасть в $i$-й элемент, нужно пройти $i$ шагов от головы. Зато вставка и удаление узла — за $O(1)$, если мы уже стоим рядом. Почти каждая задача раздела сводится к аккуратной перестановке указателей `next` за один-два прохода и $O(1)$ дополнительной памяти: скопировать список в массив почти всегда можно, но это «неспортивное» решение, которое на интервью попросят улучшить.

Техник немного, и они хорошо комбинируются: dummy node снимает edge-cases на голове, fast & slow pointers находят середину и циклы, reverse переворачивает куски списка in-place. Сложные задачи (Reorder List, LRU Cache) — это просто композиция двух-трёх базовых приёмов. Раздел тесно пересекается с [[two-pointers]]: fast & slow — это те же два указателя, только скорость разная, а не направление.

## Итеративный reverse (prev / curr / next)

**Сигнал.** В условии слово «reverse» или нужно обойти список в обратном порядке, не тратя $O(n)$ памяти на стек/массив.

**Идея.** Идём по списку и у каждого узла разворачиваем стрелку `next` назад. Чтобы не потерять хвост, храним три указателя: `prev` (уже развёрнутая часть), `curr` (текущий узел), `nxt` (сохранённый хвост). В конце `prev` — новая голова.

```python
def reverse_list(head):
    prev, curr = None, head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev, curr = curr, nxt
    return prev
```

Для reverse части списка (Reverse Linked List II) или k-групп (Reverse Nodes in k-Group) приём тот же, добавляется бухгалтерия: запоминаем узел перед разворачиваемым отрезком и после него, разворачиваем отрезок, пришиваем оба конца. В k-Group сначала проверяем указателем, что впереди есть полные $k$ узлов.

**Типовые задачи:** Reverse Linked List, Reverse Linked List II, Reverse Nodes in k-Group.

Сложность: $O(n)$ по времени, $O(1)$ по памяти.

## Dummy node

**Сигнал.** Операция может изменить или удалить голову списка: merge, удаление узлов, вставка в начало. Признак нужды — в решении без dummy появляется отдельный `if` «а вдруг это голова».

**Идея.** Заводим фиктивный узел перед головой: `dummy.next = head`. Теперь у каждого настоящего узла, включая голову, есть предшественник — и все операции пишутся единообразно, без специального случая. Возвращаем `dummy.next`, что бы ни случилось с исходной головой.

```python
def merge_two_lists(l1, l2):
    dummy = tail = ListNode()
    while l1 and l2:
        if l1.val <= l2.val:
            tail.next, l1 = l1, l1.next
        else:
            tail.next, l2 = l2, l2.next
        tail = tail.next
    tail.next = l1 or l2  # attach the leftover
    return dummy.next
```

**Типовые задачи:** Merge Two Sorted Lists, Remove Nth Node From End of List, Add Two Numbers, Remove Linked List Elements.

Сложность: $O(n)$ по времени, $O(1)$ по памяти.

## Fast & slow pointers (алгоритм Флойда)

**Сигнал.** Нужна середина списка, детекция цикла или его начало — и всё это без хеш-таблицы посещённых узлов. Шире: любой процесс вида $x \mapsto f(x)$, который рано или поздно зацикливается.

**Идея.** Два указателя стартуют с головы: `slow` шагает по одному узлу, `fast` — по два. Когда `fast` дойдёт до конца, `slow` стоит на середине. Если в списке цикл, `fast` не упрётся в `None`, а начнёт наматывать круги и обязательно догонит `slow` внутри цикла.

```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
# no cycle: slow is at the middle
# cycle: slow == fast happens inside the loop
```

**Фаза 2 (начало цикла).** Пусть $L$ — расстояние от головы до входа в цикл, $C$ — длина цикла, а встреча произошла на расстоянии $k$ от входа. Slow прошёл $L + k$, fast — вдвое больше, и лишние $L + k$ шагов fast намотал целыми кругами:

$$
2(L + k) - (L + k) = L + k = nC \quad\Rightarrow\quad L = nC - k
$$

Значит, если из точки встречи пройти $L$ шагов, мы сместимся на $k + L = nC$ от входа — то есть окажемся ровно на входе в цикл. Поэтому запускаем второй указатель с головы: оба шагают по одному, и через $L$ шагов они встречаются в начале цикла.

```python
if slow is fast:  # cycle detected, find its start
    p = head
    while p is not slow:
        p, slow = p.next, slow.next
    return p  # cycle entry
```

Приём работает и вне списков: в Find the Duplicate Number массив читается как функция `i -> nums[i]` и дубликат — это вход в цикл (альтернатива — binary search по значению, см. [[binary-search]]); в Happy Number зацикливание суммы квадратов цифр ловится теми же двумя указателями вместо set-а из [[arrays-hashing]].

**Типовые задачи:** Middle of the Linked List, Linked List Cycle, Linked List Cycle II, Find the Duplicate Number, Happy Number, Palindrome Linked List.

Сложность: $O(n)$ по времени, $O(1)$ по памяти.

## Два указателя с фиксированным зазором

**Сигнал.** Нужен «$n$-й элемент с конца» за один проход, а длина списка неизвестна.

**Идея.** Разгоняем первый указатель на $n$ шагов вперёд, затем двигаем оба синхронно. Когда передний упирается в конец, задний стоит ровно на $n$ узлов раньше. С dummy node задний останавливается на предшественнике удаляемого узла — удаление тривиально.

```python
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    lead = follow = dummy
    for _ in range(n + 1):
        lead = lead.next
    while lead:
        lead, follow = lead.next, follow.next
    follow.next = follow.next.next
    return dummy.next
```

**Типовые задачи:** Remove Nth Node From End of List.

Сложность: $O(n)$ по времени, $O(1)$ по памяти.

## Композиция: middle → reverse → merge

**Сигнал.** Нужно переупорядочить список так, что элементы берутся то с начала, то с конца — а обращаться к концу напрямую нельзя.

**Идея.** Reorder List ($L_0 \to L_n \to L_1 \to L_{n-1} \to \ldots$) собирается из трёх уже известных кубиков: fast & slow находят середину, вторая половина разворачивается итеративным reverse, затем две половины сшиваются поочерёдным merge-ом. Каждый шаг — $O(n)$ и $O(1)$ памяти, значит и вся композиция тоже.

```python
def reorder_list(head):
    slow, fast = head, head.next
    while fast and fast.next:            # 1. find middle
        slow, fast = slow.next, fast.next.next
    second = reverse_list(slow.next)     # 2. reverse second half
    slow.next = None
    first = head
    while second:                        # 3. interleave merge
        first.next, second.next, first, second = (
            second, first.next, first.next, second.next)
```

**Типовые задачи:** Reorder List, Palindrome Linked List (middle → reverse → сравнение).

Сложность: $O(n)$ по времени, $O(1)$ по памяти.

## Копирование списка с random pointer

**Сигнал.** Deep copy структуры, где узлы ссылаются друг на друга произвольно: пока не созданы все копии, непонятно, куда вести `random`.

**Идея.** Два прохода и hashmap `old -> new` (родственно [[arrays-hashing]]): первым проходом создаём копии узлов, вторым — расставляем `next` и `random` через словарь. Ключ `None: None` избавляет от проверок на конец списка.

```python
def copy_random_list(head):
    old_to_new = {None: None}
    curr = head
    while curr:
        old_to_new[curr] = Node(curr.val)
        curr = curr.next
    curr = head
    while curr:
        old_to_new[curr].next = old_to_new[curr.next]
        old_to_new[curr].random = old_to_new[curr.random]
        curr = curr.next
    return old_to_new[head]
```

Есть вариант за $O(1)$ памяти (interleaving): копию каждого узла вставляем сразу после оригинала (`A -> A' -> B -> B'`), тогда `A'.random = A.random.next`, а третьим проходом списки расплетаются. Роль hashmap играет сама структура списка.

**Типовые задачи:** Copy List with Random Pointer.

Сложность: $O(n)$ по времени, $O(n)$ по памяти (или $O(1)$ в interleaving-варианте).

## LRU Cache: hashmap + doubly linked list

**Сигнал.** Нужны `get` и `put` за $O(1)$ с вытеснением least recently used. Каждая структура по отдельности не справляется — нужна их пара.

**Идея.** Hashmap даёт $O(1)$ доступ по ключу, но не хранит порядок использования. Doubly linked list хранит порядок и умеет за $O(1)$ удалить узел из середины и вставить в голову — но только если узел уже в руках. Поэтому hashmap хранит указатели прямо на узлы списка: нашли узел за $O(1)$, переставили в голову за $O(1)$. Вытесняем с хвоста. Два sentinel-узла (head и tail) — это тот же трюк dummy node, убирающий edge-cases пустого списка.

```python
class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = {}                        # key -> DLL node
        self.head, self.tail = Node(), Node()  # sentinels: MRU side, LRU side
        self.head.next, self.tail.prev = self.tail, self.head
    # get: lookup in cache, unlink node, push to front
    # put: update or insert at front; if over capacity, pop tail.prev
```

**Типовые задачи:** LRU Cache, LFU Cache (усложнение: hashmap частот, по DLL на частоту).

Сложность: $O(1)$ на операцию, $O(\text{capacity})$ по памяти.

## Merge K Sorted Lists

**Сигнал.** Слить $k$ отсортированных последовательностей в одну. Наивный поочерёдный merge даёт $O(Nk)$ — это сигнал, что нужен heap или divide & conquer.

**Идея.** Держим min-heap из текущих голов всех списков (подробнее — [[heap]]): извлекаем минимум, пришиваем к результату, кладём в heap следующий узел того же списка. В heap всегда не больше $k$ элементов, поэтому каждый из $N$ узлов обрабатывается за $O(\log k)$. Индекс $i$ в кортеже — tie-breaker, чтобы Python не сравнивал сами узлы при равных значениях.

```python
import heapq

def merge_k_lists(lists):
    heap = [(node.val, i, node) for i, node in enumerate(lists) if node]
    heapq.heapify(heap)
    dummy = tail = ListNode()
    while heap:
        _, i, node = heapq.heappop(heap)
        tail.next = tail = node
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next
```

Альтернатива — divide & conquer: сливаем списки парами, как в merge sort, за $\log k$ раундов по $O(N)$ каждый. Та же $O(N \log k)$, но $O(1)$ дополнительной памяти (без учёта рекурсии).

**Типовые задачи:** Merge K Sorted Lists.

Сложность: $O(N \log k)$ по времени, $O(k)$ по памяти (heap) или $O(1)$ (divide & conquer).

## Карта раздела

| Техника | Сигнал в задаче | Сложность |
| --- | --- | --- |
| Итеративный reverse | «reverse», обход с конца без лишней памяти | $O(n)$ / $O(1)$ |
| Dummy node | операция может задеть голову списка | $O(n)$ / $O(1)$ |
| Fast & slow pointers | середина, цикл, зацикливание $x \mapsto f(x)$ | $O(n)$ / $O(1)$ |
| Указатели с зазором | $n$-й с конца за один проход | $O(n)$ / $O(1)$ |
| Middle → reverse → merge | переупорядочивание «с двух концов» | $O(n)$ / $O(1)$ |
| Hashmap old → new | deep copy с произвольными ссылками | $O(n)$ / $O(n)$ |
| Hashmap + DLL | $O(1)$ доступ + $O(1)$ порядок использования | $O(1)$ на операцию |
| Heap над $k$ головами | слить $k$ отсортированных списков | $O(N \log k)$ / $O(k)$ |
