import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) - 1 for x in data[1:1 + n]]

    indeg = [0] * n
    for v in a:
        indeg[v] += 1

    # Peel off vertices with in-degree 0; remaining vertices lie on cycles.
    order = []
    dq = deque(i for i in range(n) if indeg[i] == 0)
    removed = [False] * n
    while dq:
        u = dq.popleft()
        removed[u] = True
        order.append(u)
        w = a[u]
        indeg[w] -= 1
        if indeg[w] == 0:
            dq.append(w)

    total = [0] * n
    on_cycle = [not r for r in removed]
    # Compute cycle lengths.
    visited = [False] * n
    for s in range(n):
        if on_cycle[s] and not visited[s]:
            cyc = []
            u = s
            while not visited[u]:
                visited[u] = True
                cyc.append(u)
                u = a[u]
            L = len(cyc)
            for u in cyc:
                total[u] = L

    # Tail vertices: process in reverse peel order (successor is resolved first).
    for u in reversed(order):
        total[u] = total[a[u]] + 1

    print(sum(total))


main()
