import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    edges = data[1:1 + n]
    V = 26
    adj = [[False] * V for _ in range(V)]
    bal = [0] * V
    used = [False] * V
    parent = list(range(V))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for s in edges:
        u = ord(s[0]) - 65
        v = ord(s[1]) - 65
        adj[u][v] = True
        bal[u] += 1
        bal[v] -= 1
        used[u] = used[v] = True
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv

    # transitive closure (reachability via paths of length >= 1)
    reach = [row[:] for row in adj]
    for k in range(V):
        rk = reach[k]
        for i in range(V):
            if reach[i][k]:
                ri = reach[i]
                for j in range(V):
                    if rk[j]:
                        ri[j] = True

    comps = {}
    for v in range(V):
        if used[v]:
            comps.setdefault(find(v), []).append(v)

    INF = 10 ** 9
    total = 0
    for members in comps.values():
        P = sum(bal[v] for v in members if bal[v] > 0)
        # bipartite max flow: negatives (sources) -> positives (sinks)
        # nodes: 0..V-1 vertices, S=V, T=V+1
        M = V + 2
        S, T = V, V + 1
        cap = [[0] * M for _ in range(M)]
        for q in members:
            if bal[q] < 0:
                cap[S][q] = -bal[q]
                for p in members:
                    if bal[p] > 0 and reach[q][p]:
                        cap[q][p] = INF
        for p in members:
            if bal[p] > 0:
                cap[p][T] = bal[p]
        flow = 0
        while True:
            par = [-1] * M
            par[S] = S
            dq = deque([S])
            while dq and par[T] == -1:
                x = dq.popleft()
                for y in range(M):
                    if par[y] == -1 and cap[x][y] > 0:
                        par[y] = x
                        dq.append(y)
            if par[T] == -1:
                break
            f = INF
            y = T
            while y != S:
                x = par[y]
                f = min(f, cap[x][y])
                y = x
            y = T
            while y != S:
                x = par[y]
                cap[x][y] -= f
                cap[y][x] += f
                y = x
            flow += f
        total += max(1, P - flow)
    print(total)


main()
