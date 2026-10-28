import sys
from operator import add


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    BIG = 10 ** 12  # "unreachable" sentinel (integers only, for speed)
    d = [[BIG] * n for _ in range(n)]
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

    # Floyd-Warshall (no negative cycles, so exact)
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik >= BIG // 2:
                continue
            di = d[i]
            for j in range(n):
                nv = dik + dk[j]
                if nv < di[j]:
                    di[j] = nv

    # A min-cost covering walk = min-cost Hamiltonian-style path in the
    # metric closure. Reaching v from u costs d[u][v].
    # col[v][u] = d[u][v]
    col = [[d[u][v] for u in range(n)] for v in range(n)]

    # dp[mask] = list over end vertex v: min cost of a walk covering exactly
    # the vertices of mask and ending at v (BIG if impossible); None if no
    # walk covers mask at all.
    full = (1 << n) - 1
    dp = [None] * (full + 1)
    for s in range(n):
        row = [BIG] * n
        row[s] = 0
        dp[1 << s] = row

    thr = BIG // 2
    for mask in range(1, full + 1):
        if mask & (mask - 1) == 0:
            continue  # singletons already set
        row = [BIG] * n
        any_set = False
        mm = mask
        while mm:
            lb = mm & -mm
            mm ^= lb
            v = lb.bit_length() - 1
            p = dp[mask ^ lb]
            if p is None:
                continue
            best = min(map(add, p, col[v]))
            if best < thr:
                row[v] = best
                any_set = True
        if any_set:
            dp[mask] = row

    row = dp[full]
    best = min(row) if row is not None else BIG
    if best >= thr:
        print("No")
    else:
        print(best)


main()
