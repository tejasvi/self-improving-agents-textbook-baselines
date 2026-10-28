import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) - 1 for x in data[1:1 + n]]

    indeg = [0] * n
    for v in a:
        indeg[v] += 1

    # Peel vertices not on any cycle (Kahn's algorithm).
    order = []
    q = deque(i for i in range(n) if indeg[i] == 0)
    removed = [False] * n
    while q:
        u = q.popleft()
        removed[u] = True
        order.append(u)
        w = a[u]
        indeg[w] -= 1
        if indeg[w] == 0:
            q.append(w)

    reach = [0] * n
    # Cycle vertices: reach equals the length of their cycle.
    for s in range(n):
        if removed[s] or reach[s]:
            continue
        cyc = []
        v = s
        while True:
            cyc.append(v)
            v = a[v]
            if v == s:
                break
        L = len(cyc)
        for v in cyc:
            reach[v] = L

    # Tail vertices: reach(u) = 1 + reach(a[u]); process in reverse peel order
    # so that a[u] is always resolved first.
    for u in reversed(order):
        reach[u] = reach[a[u]] + 1

    print(sum(reach))


main()
