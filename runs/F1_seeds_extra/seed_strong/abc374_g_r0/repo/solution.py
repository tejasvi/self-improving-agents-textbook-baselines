import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    names = data[1:1 + n]
    V = 26
    adj = [[False] * V for _ in range(V)]
    used = [False] * V
    parent = list(range(V))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    outd = [0] * V
    ind = [0] * V
    for s in names:
        a = ord(s[0]) - 65
        b = ord(s[1]) - 65
        adj[a][b] = True
        used[a] = used[b] = True
        outd[a] += 1
        ind[b] += 1
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

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

    total = 0
    INF = 10 ** 9
    for members in comps.values():
        # Build flow network: S=V, T=V+1
        N = V + 2
        S, T = V, V + 1
        cap = [[0] * N for _ in range(N)]
        surplus = 0
        for v in members:
            d = outd[v] - ind[v]
            if d > 0:
                cap[v][T] = d
                surplus += d
            elif d < 0:
                cap[S][v] = -d
        for u in members:
            if outd[u] - ind[u] < 0:
                for v in members:
                    if outd[v] - ind[v] > 0 and reach[u][v]:
                        cap[u][v] = INF
        flow = 0
        while True:
            prev = [-1] * N
            prev[S] = S
            q = deque([S])
            while q and prev[T] == -1:
                x = q.popleft()
                for y in range(N):
                    if prev[y] == -1 and cap[x][y] > 0:
                        prev[y] = x
                        q.append(y)
            if prev[T] == -1:
                break
            # bottleneck
            f = INF
            y = T
            while y != S:
                x = prev[y]
                f = min(f, cap[x][y])
                y = x
            y = T
            while y != S:
                x = prev[y]
                cap[x][y] -= f
                cap[y][x] += f
                y = x
            flow += f
        total += max(1, surplus - flow)
    print(total)


main()
