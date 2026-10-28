import sys
from operator import add


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    INF = float("inf")
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
    # Floyd-Warshall (graph has no negative cycles)
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik == INF:
                continue
            di = d[i]
            for j in range(n):
                nv = dik + dk[j]
                if nv < di[j]:
                    di[j] = nv

    BIG = 10 ** 15  # sentinel for unreachable (finite arithmetic)
    # col[j][i] = dist(i -> j), unreachable -> BIG
    col = [[(d[i][j] if d[i][j] != INF else BIG) for i in range(n)]
           for j in range(n)]
    UNSET = 4 * BIG

    full = (1 << n) - 1
    dp = [None] * (1 << n)
    base = [UNSET] * n
    for j in range(n):
        r = base[:]
        r[j] = 0
        dp[1 << j] = r
    for mask in range(1, full + 1):
        if dp[mask] is not None:
            continue
        row = base[:]
        m_ = mask
        while m_:
            lb = m_ & -m_
            m_ ^= lb
            j = lb.bit_length() - 1
            prev = dp[mask ^ lb]
            row[j] = min(map(add, prev, col[j]))
        dp[mask] = row
    ans = min(dp[full])
    if ans >= BIG // 2:
        print("No")
    else:
        print(ans)


main()
