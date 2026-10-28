import sys
from collections import deque

INF = 10**9


def min_cut(n_nodes, edges, s, t):
    # Dinic's algorithm; edges: list of (u, v, cap)
    graph = [[] for _ in range(n_nodes)]
    to = []
    cap = []
    for u, v, c in edges:
        graph[u].append(len(to))
        to.append(v); cap.append(c)
        graph[v].append(len(to))
        to.append(u); cap.append(0)
    flow = 0
    while True:
        level = [-1] * n_nodes
        level[s] = 0
        dq = deque([s])
        while dq:
            x = dq.popleft()
            for e in graph[x]:
                if cap[e] > 0 and level[to[e]] < 0:
                    level[to[e]] = level[x] + 1
                    dq.append(to[e])
        if level[t] < 0:
            return flow
        it = [0] * n_nodes

        def dfs(x, f):
            if x == t:
                return f
            while it[x] < len(graph[x]):
                e = graph[x][it[x]]
                y = to[e]
                if cap[e] > 0 and level[y] == level[x] + 1:
                    d = dfs(y, min(f, cap[e]))
                    if d > 0:
                        cap[e] -= d
                        cap[e ^ 1] += d
                        return d
                it[x] += 1
            return 0

        while True:
            f = dfs(s, INF * 10)
            if f == 0:
                break
            flow += f
            if flow >= INF:
                return flow


def cost_for_D(N, E, D):
    # min number of edges with p_v > p_u, over potentials p in [0..D],
    # p_1 = 0, p_N = D, p_v - p_u <= 1 for every edge u->v.
    def nid(v, k):  # k in 1..D
        return v * D + (k - 1)
    s = N * D
    t = s + 1
    edges = []
    for v in range(N):
        for k in range(2, D + 1):
            edges.append((nid(v, k), nid(v, k - 1), INF))
    for k in range(1, D + 1):
        edges.append((nid(0, k), t, INF))
        edges.append((s, nid(N - 1, k), INF))
    for u, v in E:
        for k in range(1, D + 1):
            edges.append((nid(v, k), nid(u, k), 1))
        for k in range(2, D + 1):
            edges.append((nid(v, k), nid(u, k - 1), INF))
    return min_cut(N * D + 2, edges, s, t)


def main():
    data = sys.stdin.read().split()
    N, M, K = int(data[0]), int(data[1]), int(data[2])
    E = []
    for j in range(M):
        u = int(data[3 + 2 * j]) - 1
        v = int(data[4 + 2 * j]) - 1
        E.append((u, v))
    best = 0
    for D in range(1, N):
        c = cost_for_D(N, E, D)
        if c <= K:
            best = D
    print(best)


if __name__ == "__main__":
    main()
