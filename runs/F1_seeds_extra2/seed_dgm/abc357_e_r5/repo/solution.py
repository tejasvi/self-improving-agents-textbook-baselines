import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) - 1 for x in data[1:1 + n]]

    indeg = [0] * n
    for v in a:
        indeg[v] += 1

    # Peel off vertices with in-degree 0 (tree vertices); remaining are on cycles.
    order = []
    dq = deque(i for i in range(n) if indeg[i] == 0)
    while dq:
        u = dq.popleft()
        order.append(u)
        v = a[u]
        indeg[v] -= 1
        if indeg[v] == 0:
            dq.append(v)

    f = [0] * n
    on_cycle = [indeg[i] > 0 for i in range(n)]
    for s in range(n):
        if on_cycle[s] and f[s] == 0:
            cyc = []
            u = s
            while f[u] == 0 and on_cycle[u]:
                f[u] = -1  # mark visiting
                cyc.append(u)
                u = a[u]
            L = len(cyc)
            for c in cyc:
                f[c] = L

    # Tree vertices: process in reverse peel order (successor is resolved first).
    for u in reversed(order):
        f[u] = 1 + f[a[u]]

    print(sum(f))


main()
