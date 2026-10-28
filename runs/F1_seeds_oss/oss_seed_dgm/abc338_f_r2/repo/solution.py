# Solution for "Negative Traveling Salesman"
# We need the minimum total weight of a walk that visits every vertex at least once.
# Since we may repeat vertices and edges, the optimal walk can be seen as a permutation
# of the vertices where between consecutive vertices we travel along the shortest path.
# Therefore we first compute all‑pairs shortest path distances (graph has no negative cycles).
# Then we run a DP over subsets (Held‑Karp) on the directed metric.

import sys

def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    INF = 10**18
    # distance matrix
    dist = [[INF] * N for _ in range(N)]
    for i in range(N):
        dist[i][i] = 0
    for _ in range(M):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        w = int(next(it))
        if w < dist[u][v]:
            dist[u][v] = w
    # Floyd‑Warshall (no negative cycles per statement)
    for k in range(N):
        dk = dist[k]
        for i in range(N):
            dik = dist[i][k]
            if dik == INF:
                continue
            row_i = dist[i]
            nd_base = dik
            for j in range(N):
                nd = nd_base + dk[j]
                if nd < row_i[j]:
                    row_i[j] = nd
    ALL = 1 << N
    dp = [[INF] * N for _ in range(ALL)]
    for v in range(N):
        dp[1 << v][v] = 0  # start at v, visited only v, cost 0
    for mask in range(ALL):
        # iterate over current end vertex
        for v in range(N):
            cur = dp[mask][v]
            if cur == INF:
                continue
            # try to add a new vertex u not yet visited
            not_visited = (~mask) & (ALL - 1)
            u_mask = not_visited
            while u_mask:
                lsb = u_mask & -u_mask
                u = (lsb.bit_length() - 1)
                d = dist[v][u]
                if d != INF:
                    nmask = mask | lsb
                    nd = cur + d
                    if nd < dp[nmask][u]:
                        dp[nmask][u] = nd
                u_mask -= lsb
    full = ALL - 1
    ans = min(dp[full])
    if ans == INF:
        print("No")
    else:
        print(ans)

if __name__ == "__main__":
    solve()
