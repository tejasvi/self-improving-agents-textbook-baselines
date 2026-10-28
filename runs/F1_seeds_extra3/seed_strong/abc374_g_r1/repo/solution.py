import sys
from collections import deque


def max_flow(n, cap, s, t):
    flow = 0
    while True:
        par = [-1] * n
        par[s] = s
        dq = deque([s])
        while dq and par[t] == -1:
            x = dq.popleft()
            for y in range(n):
                if par[y] == -1 and cap[x][y] > 0:
                    par[y] = x
                    dq.append(y)
        if par[t] == -1:
            return flow
        f = float('inf')
        y = t
        while y != s:
            x = par[y]
            f = min(f, cap[x][y])
            y = x
        y = t
        while y != s:
            x = par[y]
            cap[x][y] -= f
            cap[y][x] += f
            y = x
        flow += f


def solve(pairs):
    V = 26
    adj = [[False] * V for _ in range(V)]
    parent = list(range(V))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    used = [False] * V
    bal = [0] * V
    for s in pairs:
        u = ord(s[0]) - 65
        v = ord(s[1]) - 65
        adj[u][v] = True
        used[u] = used[v] = True
        bal[u] += 1
        bal[v] -= 1
        parent[find(u)] = find(v)

    # transitive closure (paths of length >= 1)
    reach = [row[:] for row in adj]
    for k in range(V):
        for i in range(V):
            if reach[i][k]:
                rk = reach[k]
                ri = reach[i]
                for j in range(V):
                    if rk[j]:
                        ri[j] = True

    comps = {}
    for x in range(V):
        if used[x]:
            comps.setdefault(find(x), []).append(x)

    total = 0
    INF = 10 ** 9
    for vs in comps.values():
        P = sum(bal[x] for x in vs if bal[x] > 0)
        # network: source=0, sink=1, deficit nodes, surplus nodes
        m = len(vs)
        n = m + 2
        S, T = 0, 1
        cap = [[0] * n for _ in range(n)]
        for i, x in enumerate(vs):
            if bal[x] < 0:
                cap[S][2 + i] = -bal[x]
            elif bal[x] > 0:
                cap[2 + i][T] = bal[x]
        for i, x in enumerate(vs):
            if bal[x] >= 0:
                continue
            for j, y in enumerate(vs):
                if bal[y] > 0 and reach[x][y]:
                    cap[2 + i][2 + j] = INF
        F = max_flow(n, cap, S, T)
        total += max(1, P - F)
    return total


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    print(solve(data[1:1 + n]))


if __name__ == "__main__":
    main()
