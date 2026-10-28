import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = [int(x) - 1 for x in data[1:1 + n]]

    indeg = [0] * n
    for x in a:
        indeg[x] += 1

    # Peel vertices with in-degree 0; remaining vertices lie on cycles.
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        v = a[u]
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)

    removed = [False] * n
    for u in order:
        removed[u] = True

    f = [0] * n
    # Cycle vertices: f = cycle length.
    visited = [False] * n
    for i in range(n):
        if not removed[i] and not visited[i]:
            cyc = []
            j = i
            while not visited[j]:
                visited[j] = True
                cyc.append(j)
                j = a[j]
            L = len(cyc)
            for c in cyc:
                f[c] = L

    # Tail vertices: process in reverse peel order so a[u] is already known.
    for u in reversed(order):
        f[u] = 1 + f[a[u]]

    print(sum(f))


main()
