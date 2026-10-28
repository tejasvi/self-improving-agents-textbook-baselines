import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) - 1 for x in data[1:1 + n]]

    indeg = [0] * n
    for v in a:
        indeg[v] += 1

    # Peel off tree vertices (Kahn's algorithm); remaining vertices lie on cycles.
    order = []
    dq = deque(i for i in range(n) if indeg[i] == 0)
    while dq:
        u = dq.popleft()
        order.append(u)
        v = a[u]
        indeg[v] -= 1
        if indeg[v] == 0:
            dq.append(v)

    reach = [0] * n
    on_cycle = [indeg[i] > 0 for i in range(n)]
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
                reach[u] = L

    for u in reversed(order):
        reach[u] = reach[a[u]] + 1

    print(sum(reach))


main()
