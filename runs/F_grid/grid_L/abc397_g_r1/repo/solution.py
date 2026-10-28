import sys
from collections import deque


def feasible(N, edges, K, D):
    # Check whether there is p: V -> [0, D], p(1)=0, p(N)=D, p(v) <= p(u)+1 for
    # every edge u->v, with sum over edges of max(0, p(v)-p(u)) <= K.
    # Solved as a min cut: node (v,k) on source side <=> p(v) >= k, k=1..D.
    if D == 0:
        return True
    INF = 10 ** 9
    V = N * D + 2
    s, t = N * D, N * D + 1

    def node(v, k):  # v 0-indexed, k in 1..D
        return v * D + (k - 1)

    graph = [[] for _ in range(V)]

    def add(a, b, c):
        graph[a].append([b, c, len(graph[b])])
        graph[b].append([a, 0, len(graph[a]) - 1])

    for v in range(N):
        for k in range(1, D):
            add(node(v, k + 1), node(v, k), INF)  # p(v)>=k+1 => p(v)>=k
    for k in range(1, D + 1):
        add(node(0, k), t, INF)  # p(1) = 0
    add(s, node(N - 1, D), INF)  # p(N) >= D
    for u, v in edges:
        for k in range(2, D + 1):
            add(node(v, k), node(u, k - 1), INF)  # p(v)>=k => p(u)>=k-1
        for k in range(1, D + 1):
            add(node(v, k), node(u, k), 1)  # cost if p(v)>=k>p(u)

    flow = 0
    while True:
        prev = [None] * V
        prev[s] = (-1, -1)
        dq = deque([s])
        while dq and prev[t] is None:
            x = dq.popleft()
            for i, (y, c, r) in enumerate(graph[x]):
                if c > 0 and prev[y] is None:
                    prev[y] = (x, i)
                    dq.append(y)
        if prev[t] is None:
            break
        # bottleneck
        b = INF * 10
        y = t
        while y != s:
            x, i = prev[y]
            b = min(b, graph[x][i][1])
            y = x
        y = t
        while y != s:
            x, i = prev[y]
            e = graph[x][i]
            e[1] -= b
            graph[y][e[2]][1] += b
            y = x
        flow += b
        if flow > K:
            return False
    return flow <= K


def main():
    data = sys.stdin.read().split()
    N, M, K = int(data[0]), int(data[1]), int(data[2])
    edges = []
    idx = 3
    for _ in range(M):
        u = int(data[idx]) - 1
        v = int(data[idx + 1]) - 1
        idx += 2
        edges.append((u, v))
    best = 0
    for D in range(1, N):
        if feasible(N, edges, K, D):
            best = D
    print(best)


main()
