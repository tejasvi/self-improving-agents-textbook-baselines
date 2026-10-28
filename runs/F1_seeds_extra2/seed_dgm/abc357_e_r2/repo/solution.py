import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) - 1 for x in data[1:1 + n]]

    # Peel off vertices with in-degree 0; the remaining vertices lie on cycles.
    indeg = [0] * n
    for v in a:
        indeg[v] += 1
    removed = [False] * n
    dq = deque(i for i in range(n) if indeg[i] == 0)
    while dq:
        u = dq.popleft()
        removed[u] = True
        w = a[u]
        indeg[w] -= 1
        if indeg[w] == 0:
            dq.append(w)
    on_cycle = [not r for r in removed]

    # Cycle length for each cycle vertex.
    cyc_len = [0] * n
    seen = [False] * n
    for s in range(n):
        if on_cycle[s] and not seen[s]:
            cyc = []
            x = s
            while not seen[x]:
                seen[x] = True
                cyc.append(x)
                x = a[x]
            L = len(cyc)
            for x in cyc:
                cyc_len[x] = L

    # Reverse graph; BFS from cycle vertices to compute tail depths.
    radj_head = [-1] * n
    nxt = [-1] * n
    for u in range(n):
        v = a[u]
        nxt[u] = radj_head[v]
        radj_head[v] = u

    depth = [0] * n
    total = 0
    q = deque(i for i in range(n) if on_cycle[i])
    while q:
        v = q.popleft()
        total += depth[v] + cyc_len[v]
        u = radj_head[v]
        while u != -1:
            if not on_cycle[u]:
                depth[u] = depth[v] + 1
                cyc_len[u] = cyc_len[v]
                q.append(u)
            u = nxt[u]

    print(total)


main()
