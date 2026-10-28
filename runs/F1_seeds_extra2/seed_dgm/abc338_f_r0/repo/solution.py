import sys
from operator import add


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    BIG = 1 << 60
    LIM = 1 << 59
    d = [[BIG] * n for _ in range(n)]
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
    for k in range(n):
        dk = d[k]
        for i in range(n):
            di = d[i]
            dik = di[k]
            if dik >= LIM:
                continue
            for j in range(n):
                nv = dik + dk[j]
                if nv < di[j]:
                    di[j] = nv
    # col[u][v] = dist v->u, clamp unreachable to BIG
    col = [[d[v][u] for v in range(n)] for u in range(n)]

    layer = {}
    for v in range(n):
        row = [BIG] * n
        row[v] = 0
        layer[1 << v] = row
    full = (1 << n) - 1
    for _ in range(1, n):
        nxt = {}
        get = nxt.get
        for mask, row in layer.items():
            for u in range(n):
                bit = 1 << u
                if mask & bit:
                    continue
                best = min(map(add, row, col[u]))
                if best >= LIM:
                    continue
                nm = mask | bit
                nrow = get(nm)
                if nrow is None:
                    nrow = [BIG] * n
                    nxt[nm] = nrow
                if best < nrow[u]:
                    nrow[u] = best
        layer = nxt
    row = layer.get(full)
    if row is None:
        print("No")
        return
    ans = min(row)
    print("No" if ans >= LIM else ans)


main()
