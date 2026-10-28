import sys
from collections import deque


def max_flow(n, cap, s, t):
    # cap: n x n matrix (list of lists), Edmonds-Karp
    flow = 0
    while True:
        par = [-1] * n
        par[s] = s
        q = deque([s])
        while q and par[t] == -1:
            u = q.popleft()
            for v in range(n):
                if par[v] == -1 and cap[u][v] > 0:
                    par[v] = u
                    q.append(v)
        if par[t] == -1:
            return flow
        # bottleneck
        b = float('inf')
        v = t
        while v != s:
            u = par[v]
            b = min(b, cap[u][v])
            v = u
        v = t
        while v != s:
            u = par[v]
            cap[u][v] -= b
            cap[v][u] += b
            v = u
        flow += b


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    names = data[1:1 + n]
    INF = 10 ** 9
    adj = [[0] * 26 for _ in range(26)]
    outd = [0] * 26
    ind = [0] * 26
    parent = list(range(26))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    used = [False] * 26
    for s in names:
        a = ord(s[0]) - 65
        b = ord(s[1]) - 65
        adj[a][b] = 1
        outd[a] += 1
        ind[b] += 1
        used[a] = used[b] = True
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    ex = [outd[v] - ind[v] for v in range(26)]
    comps = {}
    for v in range(26):
        if used[v]:
            comps.setdefault(find(v), []).append(v)

    total = 0
    for vs in comps.values():
        k = len(vs)
        N = k + 2
        S, T = k, k + 1
        cap = [[0] * N for _ in range(N)]
        P = 0
        for i, u in enumerate(vs):
            for j, v in enumerate(vs):
                if adj[u][v]:
                    cap[i][j] = INF
            if ex[u] > 0:
                P += ex[u]
                cap[i][T] = ex[u]
            elif ex[u] < 0:
                cap[S][i] = -ex[u]
        F = max_flow(N, cap, S, T)
        total += max(1, P - F)
    print(total)


main()
