import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    edges = data[1:1 + n]
    adj_edges = []
    out = [0] * 26
    inn = [0] * 26
    parent = list(range(26))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    used = [False] * 26
    for s in edges:
        u = ord(s[0]) - 65
        v = ord(s[1]) - 65
        adj_edges.append((u, v))
        out[u] += 1
        inn[v] += 1
        used[u] = used[v] = True
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv

    comps = {}
    for x in range(26):
        if used[x]:
            comps.setdefault(find(x), []).append(x)

    INF = 10 ** 9
    total = 0
    for root, verts in comps.items():
        # node indices: local mapping; S and T appended
        idx = {v: i for i, v in enumerate(verts)}
        m = len(verts)
        S, T = m, m + 1
        N = m + 2
        cap = [[0] * N for _ in range(N)]
        for u, v in adj_edges:
            if u in idx and find(u) == root:
                cap[idx[u]][idx[v]] = INF
        P = 0
        for v in verts:
            e = out[v] - inn[v]
            if e < 0:
                cap[S][idx[v]] = -e
            elif e > 0:
                cap[idx[v]][T] = e
                P += e
        # Edmonds-Karp
        F = 0
        while True:
            prev = [-1] * N
            prev[S] = S
            dq = deque([S])
            while dq and prev[T] == -1:
                x = dq.popleft()
                for y in range(N):
                    if prev[y] == -1 and cap[x][y] > 0:
                        prev[y] = x
                        dq.append(y)
            if prev[T] == -1:
                break
            # bottleneck
            b = INF
            y = T
            while y != S:
                x = prev[y]
                b = min(b, cap[x][y])
                y = x
            y = T
            while y != S:
                x = prev[y]
                cap[x][y] -= b
                cap[y][x] += b
                y = x
            F += b
        total += max(1, P - F)
    print(total)

main()
