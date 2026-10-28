import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = [int(x) - 1 for x in data[1:1 + n]]

    indeg = [0] * n
    for x in a:
        indeg[x] += 1

    # Peel off nodes with in-degree 0; remaining nodes lie on cycles.
    order = []
    q = deque(i for i in range(n) if indeg[i] == 0)
    removed = [False] * n
    while q:
        u = q.popleft()
        removed[u] = True
        order.append(u)
        v = a[u]
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)

    reach = [0] * n
    on_cycle = [not r for r in removed]

    # Cycle lengths.
    seen = [False] * n
    for i in range(n):
        if on_cycle[i] and not seen[i]:
            cyc = []
            j = i
            while not seen[j]:
                seen[j] = True
                cyc.append(j)
                j = a[j]
            L = len(cyc)
            for j in cyc:
                reach[j] = L

    # Tail vertices: reach(u) = 1 + reach(a[u]); a[u] is processed first in reverse order.
    for u in reversed(order):
        reach[u] = 1 + reach[a[u]]

    print(sum(reach))


main()
