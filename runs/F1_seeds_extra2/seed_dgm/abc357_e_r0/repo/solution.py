import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) - 1 for x in data[1:1 + n]]

    indeg = [0] * n
    for x in a:
        indeg[x] += 1

    # Peel off vertices not on any cycle (Kahn's algorithm).
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
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
    # Cycle vertices: reach equals cycle length.
    on_cycle = [not removed[i] for i in range(n)]
    seen = [False] * n
    for s in range(n):
        if on_cycle[s] and not seen[s]:
            length = 0
            v = s
            while not seen[v]:
                seen[v] = True
                length += 1
                v = a[v]
            v = s
            for _ in range(length):
                reach[v] = length
                v = a[v]

    # Tree vertices: process in reverse peel order so a[u] is done first.
    for u in reversed(order):
        reach[u] = 1 + reach[a[u]]

    print(sum(reach))


main()
