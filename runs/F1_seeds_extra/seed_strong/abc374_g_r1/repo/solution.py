import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    names = data[1:1 + n]
    V = 26
    adj = [[False] * V for _ in range(V)]
    d = [0] * V
    used = [False] * V
    parent = list(range(V))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for s in names:
        u = ord(s[0]) - 65
        v = ord(s[1]) - 65
        adj[u][v] = True
        d[u] += 1
        d[v] -= 1
        used[u] = used[v] = True
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv

    # transitive closure (reachability by paths of length >= 1)
    reach = [row[:] for row in adj]
    for k in range(V):
        rk = reach[k]
        for i in range(V):
            if reach[i][k]:
                ri = reach[i]
                for j in range(V):
                    if rk[j]:
                        ri[j] = True

    # group by component
    comps = {}
    for v in range(V):
        if used[v]:
            comps.setdefault(find(v), []).append(v)

    total = 0
    for nodes in comps.values():
        # max flow: source -> negative nodes (cap -d) -> reachable positive nodes -> sink (cap d)
        neg = [v for v in nodes if d[v] < 0]
        pos = [v for v in nodes if d[v] > 0]
        sumpos = sum(d[v] for v in pos)
        # build flow network
        M = len(nodes)
        idx = {v: i + 2 for i, v in enumerate(nodes)}
        N = M + 2
        S, T = 0, 1
        graph = [[] for _ in range(N)]

        def add(a, b, c):
            graph[a].append([b, c, len(graph[b])])
            graph[b].append([a, 0, len(graph[a]) - 1])

        INF = 10 ** 9
        for p in neg:
            add(S, idx[p], -d[p])
        for q in pos:
            add(idx[q], T, d[q])
        for p in neg:
            for q in pos:
                if reach[p][q]:
                    add(idx[p], idx[q], INF)
        flow = 0
        while True:
            level = [-1] * N
            level[S] = 0
            dq = deque([S])
            while dq:
                x = dq.popleft()
                for y, c, _ in graph[x]:
                    if c > 0 and level[y] < 0:
                        level[y] = level[x] + 1
                        dq.append(y)
            if level[T] < 0:
                break
            it = [0] * N

            def dfs(x, f):
                if x == T:
                    return f
                while it[x] < len(graph[x]):
                    e = graph[x][it[x]]
                    y, c, r = e
                    if c > 0 and level[y] == level[x] + 1:
                        got = dfs(y, min(f, c))
                        if got > 0:
                            e[1] -= got
                            graph[y][r][1] += got
                            return got
                    it[x] += 1
                return 0

            while True:
                f = dfs(S, INF)
                if f == 0:
                    break
                flow += f
        total += max(1, sumpos - flow)
    print(total)


main()
