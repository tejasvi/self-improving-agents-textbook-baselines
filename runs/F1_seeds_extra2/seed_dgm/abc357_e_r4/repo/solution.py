import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) - 1 for x in data[1:1 + n]]

    indeg = [0] * n
    for v in a:
        indeg[v] += 1

    # Peel off tree vertices (repeatedly remove in-degree-zero vertices).
    order = []
    q = deque(i for i in range(n) if indeg[i] == 0)
    while q:
        u = q.popleft()
        order.append(u)
        w = a[u]
        indeg[w] -= 1
        if indeg[w] == 0:
            q.append(w)

    # Remaining vertices with indeg > 0 are exactly the cycle vertices.
    depth = [0] * n
    visited = [False] * n
    for s in range(n):
        if indeg[s] > 0 and not visited[s]:
            cyc = [s]
            visited[s] = True
            v = a[s]
            while v != s:
                visited[v] = True
                cyc.append(v)
                v = a[v]
            L = len(cyc)
            for c in cyc:
                depth[c] = L

    # Tree vertices: reach themselves plus everything their successor reaches.
    for u in reversed(order):
        depth[u] = depth[a[u]] + 1

    print(sum(depth))


main()
