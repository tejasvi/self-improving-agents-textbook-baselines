# Write your solution here. Read from stdin, write to stdout.
import sys

def solve():
    import sys
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    INF = 10**15
    # 0-indexed
    dist = [[INF]*N for _ in range(N)]
    for i in range(N):
        dist[i][i] = 0
    for _ in range(M):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        w = int(next(it))
        if w < dist[u][v]:
            dist[u][v] = w
    # Floyd-Warshall for all-pairs shortest paths
    for k in range(N):
        dk = dist[k]
        for i in range(N):
            di = dist[i]
            ik = di[k]
            if ik == INF:
                continue
            # unroll inner loop
            for j in range(N):
                nd = ik + dk[j]
                if nd < di[j]:
                    di[j] = nd
    # DP over subsets for Hamiltonian path using shortest distances
    full_mask = (1 << N) - 1
    dp = [[INF]*N for _ in range(1<<N)]
    for v in range(N):
        dp[1<<v][v] = 0  # start at v
    for mask in range(1<<N):
        # iterate over last vertex v in mask
        for v in range(N):
            cur = dp[mask][v]
            if cur == INF:
                continue
            # try to go to a not yet visited u
            for u in range(N):
                if mask & (1<<u):
                    continue
                dvu = dist[v][u]
                if dvu == INF:
                    continue
                nmask = mask | (1<<u)
                nd = cur + dvu
                if nd < dp[nmask][u]:
                    dp[nmask][u] = nd
    ans = INF
    for v in range(N):
        if dp[full_mask][v] < ans:
            ans = dp[full_mask][v]
    if ans == INF:
        print("No")
    else:
        print(ans)

if __name__ == "__main__":
    solve()
