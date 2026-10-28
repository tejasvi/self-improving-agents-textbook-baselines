import sys
from operator import add


def main():
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    # Sentinel for "no path". Real path weights lie in [-19e6, 19e6].
    NO = 10 ** 9
    d = [[NO] * n for _ in range(n)]
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
    # Floyd-Warshall (no negative cycles). Skip unreachable entries explicitly.
    for k in range(n):
        dk = d[k]
        for i in range(n):
            di = d[i]
            dik = di[k]
            if dik >= NO:
                continue
            for j in range(n):
                if dk[j] >= NO:
                    continue
                nv = dik + dk[j]
                if nv < di[j]:
                    di[j] = nv
    # Answer = min over vertex orders of sum of shortest distances between
    # consecutive vertices, where the walk must reach each vertex in turn.
    # dcol[u][v] = d[v][u] : cost of moving from v into u.
    # Unreachable pairs get a large sentinel INF so sums stay huge.
    INF = 10 ** 15
    dcol = [[(d[v][u] if d[v][u] < NO else INF) for v in range(n)] for u in range(n)]
    full = (1 << n) - 1
    # Layered DP by popcount: cur[mask] = list over end vertex u of min cost
    # of a walk covering exactly mask and ending at u.
    cur = {}
    for i in range(n):
        row = [INF] * n
        row[i] = 0
        cur[1 << i] = row
    for _ in range(n - 1):
        nxt = {}
        for pm, prow in cur.items():
            for v in range(n):
                bit = 1 << v
                if pm & bit:
                    continue
                # extend walk ending at any u in pm by moving to v
                # new_row[v] = min over u of prow[u] + d(u -> v)
                c = min(map(add, prow, dcol[v]))
                nm = pm | bit
                row = nxt.get(nm)
                if row is None:
                    row = [INF] * n
                    nxt[nm] = row
                if c < row[v]:
                    row[v] = c
        cur = nxt
    dp = {full: cur[full]}
    best = min(dp[full])
    if best >= INF // 2:
        print("No")
    else:
        print(best)


main()
