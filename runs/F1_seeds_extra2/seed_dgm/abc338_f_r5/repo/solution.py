import sys
from operator import add


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    INF = 10 ** 15
    LIM = 10 ** 14  # any real walk cost is far below this in magnitude
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    p = 2
    for _ in range(m):
        u = int(data[p]) - 1
        v = int(data[p + 1]) - 1
        w = int(data[p + 2])
        p += 3
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
    # clamp unreachable to INF
    for i in range(n):
        for j in range(n):
            if d[i][j] > LIM:
                d[i][j] = INF
    # columns: col[w][v] = d[v][w]
    col = [[d[v][w] for v in range(n)] for w in range(n)]

    full = (1 << n) - 1
    dp = [None] * (1 << n)
    dp[0] = [INF] * n
    for S in range(1, full + 1):
        row = [INF] * n
        bits = S
        while bits:
            lb = bits & -bits
            w = lb.bit_length() - 1
            bits ^= lb
            prev = S ^ lb
            if prev == 0:
                row[w] = 0
                continue
            pr = dp[prev]
            best = min(map(add, pr, col[w]))
            if best < LIM:
                row[w] = best
        dp[S] = row
    final = dp[full]
    e = [min(d[v]) for v in range(n)]
    ans = None
    for v in range(n):
        if final[v] < LIM:
            cand = final[v] + e[v]
            if ans is None or cand < ans:
                ans = cand
    if ans is None:
        print("No")
    else:
        print(ans)


main()
