import sys
from operator import add


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    INF = 1 << 60
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    idx = 2
    for _ in range(m):
        u = int(data[idx]) - 1
        v = int(data[idx + 1]) - 1
        w = int(data[idx + 2])
        idx += 3
        if w < d[u][v]:
            d[u][v] = w
    # Floyd-Warshall (no negative cycles)
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik >= INF:
                continue
            di = d[i]
            for j in range(n):
                nd = dik + dk[j]
                if nd < di[j]:
                    di[j] = nd
    # Cost matrix for Hamiltonian path in the metric closure.
    # col[v][u] = cost of going u -> v (u != v); INF if unreachable or u == v.
    col = [[INF] * n for _ in range(n)]
    for v in range(n):
        for u in range(n):
            if u != v and d[u][v] < INF:
                col[v][u] = d[u][v]
    full = (1 << n) - 1

    # Group masks by popcount.
    layers = [[] for _ in range(n + 1)]
    for mask in range(1, full + 1):
        layers[bin(mask).count("1")].append(mask)

    # dp[mask] = list over end vertex v of min cost of a path visiting exactly mask ending at v.
    prev = {}
    for v in range(n):
        lst = [INF] * n
        lst[v] = 0
        prev[1 << v] = lst
    for k in range(2, n + 1):
        cur = {}
        for mask in layers[k]:
            res = [INF] * n
            mm = mask
            while mm:
                low = mm & -mm
                mm ^= low
                v = low.bit_length() - 1
                pl = prev.get(mask ^ low)
                if pl is None:
                    continue
                best = min(map(add, pl, col[v]))
                if best < INF:
                    res[v] = best
            cur[mask] = res
        prev = cur
    final = prev.get(full)
    if final is None:
        print("No")
        return
    ans = min(final)
    if ans >= INF:
        print("No")
    else:
        print(ans)


main()
