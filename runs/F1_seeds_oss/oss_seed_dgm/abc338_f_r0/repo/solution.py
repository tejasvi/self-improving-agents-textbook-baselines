# Solution for "Negative Traveling Salesman"
# We need to find the minimum total weight of a walk that visits every vertex at least once in a directed graph.
# Vertices: 1..N (N ≤ 20). Edge weights may be negative, but there are no negative cycles.
# The walk can start and end at any vertices, and may repeat vertices/edges.
# Approach:
#   1. Compute all‑pairs shortest path distances using Floyd‑Warshall (handles negative edges, no negative cycles).
#   2. Dynamic programming over subsets (Held‑Karp style) but store states sparsely to keep memory low.
#      dp[mask] is a dict mapping ending vertex v to minimal cost of a walk that visits exactly the vertices in mask and ends at v.
#      Initialise dp[1<<v][v] = 0 for each v.
#      Transition: from state (mask, v) we may go to an unvisited vertex u, paying dist[v][u].
#      The new mask becomes mask | (1<<u) and the walk ends at u.
#   3. The answer is min_v dp[full_mask][v]. If no such entry exists, output "No".
# Complexity: Floyd‑Warshall O(N^3) ≤ 8000, DP O(N^2 * 2^N) in worst case but with sparse dicts practical for N=20.

import sys

def solve() -> None:
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
        dist[u][v] = w
    # Floyd‑Warshall (handles negative edges, graph has no negative cycles)
    for k in range(N):
        dk = dist[k]
        for i in range(N):
            dik = dist[i][k]
            if dik == INF:
                continue
            di = dist[i]
            nd_base = dik
            for j in range(N):
                kj = dk[j]
                if kj == INF:
                    continue
                nd = nd_base + kj
                if nd < di[j]:
                    di[j] = nd
    full_mask = (1 << N) - 1
    # dp[mask] -> dict {v: min_cost ending at v}
    dp = [{} for _ in range(1 << N)]
    for v in range(N):
        dp[1 << v][v] = 0
    # iterate masks
    for mask in range(1, 1 << N):
        cur_dict = dp[mask]
        if not cur_dict:
            continue
        remaining = full_mask ^ mask
        # precompute list of bits in remaining for faster loop
        bits = []
        r = remaining
        while r:
            lsb = r & -r
            bits.append(lsb)
            r ^= lsb
        for v, cur_cost in cur_dict.items():
            # try to go to each unvisited vertex u
            for lsb in bits:
                u = (lsb.bit_length() - 1)
                dvu = dist[v][u]
                if dvu == INF:
                    continue
                nmask = mask | lsb
                nd = cur_cost + dvu
                ndict = dp[nmask]
                prev = ndict.get(u)
                if prev is None or nd < prev:
                    ndict[u] = nd
    # answer
    best = INF
    final_dict = dp[full_mask]
    for cost in final_dict.values():
        if cost < best:
            best = cost
    if best == INF:
        print("No")
    else:
        print(best)

if __name__ == "__main__":
    solve()
