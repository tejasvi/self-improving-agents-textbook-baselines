import sys
from operator import add


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    INF = 10 ** 18
    LIM = 10 ** 17
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
    # Floyd-Warshall (no negative cycles, so this is well-defined)
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik >= LIM:
                continue
            di = d[i]
            for j in range(n):
                nv = dik + dk[j]
                if nv < di[j]:
                    di[j] = nv
    # column access: col[w][v] = d[v][w]
    col = [[d[v][w] for v in range(n)] for w in range(n)]

    # Layered DP over visited-sets by popcount.
    # cur maps mask -> list dp[v] = min cost of walk visiting exactly mask, ending at v.
    cur = {}
    for v in range(n):
        row = [INF] * n
        row[v] = 0
        cur[1 << v] = row
    for _ in range(n - 1):
        nxt = {}
        for mask, row in cur.items():
            for w in range(n):
                bit = 1 << w
                if mask & bit:
                    continue
                val = min(map(add, row, col[w]))
                if val >= LIM:
                    continue
                nm = mask | bit
                tgt = nxt.get(nm)
                if tgt is None:
                    tgt = [INF] * n
                    nxt[nm] = tgt
                if val < tgt[w]:
                    tgt[w] = val
        cur = nxt
    full = (1 << n) - 1
    if full not in cur:
        print("No")
        return
    ans = min(cur[full])
    if ans >= LIM:
        print("No")
    else:
        print(ans)


main()
