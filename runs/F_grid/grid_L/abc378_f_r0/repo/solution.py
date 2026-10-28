import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    adj = [[] for _ in range(n + 1)]
    idx = 1
    for _ in range(n - 1):
        u = int(data[idx])
        v = int(data[idx + 1])
        idx += 2
        adj[u].append(v)
        adj[v].append(u)
    deg = [len(a) for a in adj]

    # Components of the subgraph induced by degree-3 vertices.
    comp = [-1] * (n + 1)
    cid = 0
    for s in range(1, n + 1):
        if deg[s] != 3 or comp[s] != -1:
            continue
        comp[s] = cid
        dq = deque([s])
        while dq:
            x = dq.popleft()
            for y in adj[x]:
                if deg[y] == 3 and comp[y] == -1:
                    comp[y] = cid
                    dq.append(y)
        cid += 1

    # Count degree-2 vertices attached to each degree-3 component.
    k = [0] * cid
    for u in range(1, n + 1):
        if deg[u] != 2:
            continue
        for y in adj[u]:
            if deg[y] == 3:
                k[comp[y]] += 1

    ans = 0
    for c in k:
        ans += c * (c - 1) // 2
    print(ans)


main()
