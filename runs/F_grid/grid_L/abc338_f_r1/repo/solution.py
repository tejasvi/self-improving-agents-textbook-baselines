import sys
from operator import add


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    INF = 10 ** 15
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
    # Floyd-Warshall (no negative cycles, so this gives exact shortest walks)
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik >= INF:
                continue
            di = d[i]
            for j in range(n):
                nd = dik + dk[j]
                if nd < di[j] and dk[j] < INF:
                    di[j] = nd
    # Walk visiting all vertices == Hamiltonian path on metric closure,
    # where any vertex may be the start.
    # Column form: col[v][u] = d[u][v]
    col = [[d[u][v] for u in range(n)] for v in range(n)]
    full = (1 << n) - 1
    # F[mask] = list over end vertex v of min cost walk covering exactly mask
    # ending at v (INF if impossible).
    F = [None] * (1 << n)
    for v in range(n):
        row = [INF] * n
        row[v] = 0
        F[1 << v] = row
    for mask in range(1, full + 1):
        if mask & (mask - 1) == 0:
            continue
        row = [INF] * n
        rest = mask
        while rest:
            low = rest & -rest
            v = low.bit_length() - 1
            rest ^= low
            prev = F[mask ^ low]
            if prev is None:
                continue
            best = min(map(add, prev, col[v]))
            if best < INF // 2:
                row[v] = best
        F[mask] = row
    ans = min(F[full])
    if ans >= INF // 2:
        print("No")
    else:
        print(ans)


main()
