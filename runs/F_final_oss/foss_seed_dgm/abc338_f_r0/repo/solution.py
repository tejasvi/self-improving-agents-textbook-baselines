# Write your solution here. Read from stdin, write to stdout.

import sys
from array import array

def solve():
    data = sys.stdin.buffer.read().split()
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
    # Floyd‑Warshall for all‑pairs shortest paths
    for k in range(N):
        dk = dist[k]
        for i in range(N):
            dik = dist[i][k]
            if dik == INF:
                continue
            di = dist[i]
            nd = dik
            for j in range(N):
                ndj = nd + dk[j]
                if ndj < di[j]:
                    di[j] = ndj
    # successors list with reachable vertices and distances
    succ = []
    for i in range(N):
        succ.append([(j, dist[i][j]) for j in range(N) if i != j and dist[i][j] < INF])
    FULL = (1 << N) - 1
    # DP: dp[mask][last] = minimum cost to start somewhere, visit vertices in mask, end at last
    dp = [array('q', [INF] * N) for _ in range(1 << N)]
    for i in range(N):
        dp[1 << i][i] = 0
    for mask in range(1 << N):
        # iterate over vertices that are the last element of the current mask
        sub = mask
        while sub:
            lsb = sub & -sub
            last = lsb.bit_length() - 1  # index of vertex
            sub ^= lsb
            cur = dp[mask][last]
            if cur == INF:
                continue
            for nxt, d in succ[last]:
                if mask >> nxt & 1:
                    continue
                nmask = mask | (1 << nxt)
                nd = cur + d
                if nd < dp[nmask][nxt]:
                    dp[nmask][nxt] = nd
    ans = INF
    final_dp = dp[FULL]
    for last in range(N):
        if final_dp[last] < ans:
            ans = final_dp[last]
    if ans == INF:
        print("No")
    else:
        print(ans)

if __name__ == "__main__":
    solve()
