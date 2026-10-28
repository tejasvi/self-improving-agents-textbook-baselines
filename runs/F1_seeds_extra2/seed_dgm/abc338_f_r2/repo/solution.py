import sys
from operator import add


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    INF = 1 << 60
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    p = 2
    for _ in range(m):
        u, v, w = int(data[p]) - 1, int(data[p + 1]) - 1, int(data[p + 2])
        p += 3
        if w < d[u][v]:
            d[u][v] = w
    # Floyd-Warshall (graph has no negative cycles)
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik >= INF:
                continue
            di = d[i]
            for j in range(n):
                if dk[j] < INF:
                    t = dik + dk[j]
                    if t < di[j]:
                        di[j] = t

    # The optimal walk visits vertices for the first time in some order
    # v_1..v_n; consecutive first visits cost at least d[v_i][v_{i+1}], and
    # after the last first visit a (possibly negative) tail is added.
    # dp over (mask of first-visited vertices, last vertex).
    # State for mask: list of (vertex, cost) pairs for finite entries.
    full = (1 << n) - 1
    # colget[u] = d[v][u] indexed by v
    colget = [[d[v][u] for v in range(n)].__getitem__ for u in range(n)]
    # states[mask] = (vs, cs): vertices in mask ending there, and costs
    states = [None] * (1 << n)
    for s in range(n):
        states[1 << s] = ([s], [0])
    for mask in range(1, full):
        st = states[mask]
        if st is None:
            continue
        states[mask] = None
        vs, cs = st
        for u in range(n):
            bit = 1 << u
            if mask & bit:
                continue
            g = colget[u]
            best = min(map(add, cs, map(g, vs)))
            nm = mask | bit
            nst = states[nm]
            if nst is None:
                states[nm] = ([u], [best])
            else:
                nst[0].append(u)
                nst[1].append(best)
    ans = states[full]
    res = INF
    if ans is not None:
        vs, cs = ans
        for v, c in zip(vs, cs):
            res = min(res, c + min(d[v]))
    if res >= INF // 2:
        print("No")
    else:
        print(res)


main()
