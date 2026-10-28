import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    rows = data[1:1 + n]
    # inl[c][v] = list of u with edge u->v labeled c
    # outs[u] = list of (c, mask of v) with edge u->v labeled c
    inl = [[[] for _ in range(n)] for _ in range(26)]
    outs = [dict() for _ in range(n)]
    edges = []
    for u in range(n):
        r = rows[u]
        for v in range(n):
            ch = r[v]
            if ch != '-':
                c = ord(ch) - 97
                inl[c][v].append(u)
                outs[u][c] = outs[u].get(c, 0) | (1 << v)
                edges.append((u, v))
    outs = [list(d.items()) for d in outs]

    INF = 1 << 30
    ans = [[INF] * n for _ in range(n)]  # best length for each parity

    for p in (0, 1):
        dist = [[-1] * n for _ in range(n)]
        vis = [0] * n
        F = [0] * n
        if p == 0:
            for u in range(n):
                F[u] |= 1 << u
                vis[u] |= 1 << u
                dist[u][u] = 0
        else:
            for u, v in edges:
                F[u] |= 1 << v
                vis[u] |= 1 << v
                dist[u][v] = 0
        k = 0
        while any(F):
            newbits = [0] * n
            for xp in range(n):
                f = F[xp]
                while f:
                    b = f & -f
                    yp = b.bit_length() - 1
                    f ^= b
                    for c, mask in outs[yp]:
                        for x in inl[c][xp]:
                            newbits[x] |= mask
            k += 1
            F = [0] * n
            for x in range(n):
                nb = newbits[x] & ~vis[x]
                if nb:
                    vis[x] |= nb
                    F[x] = nb
                    dx = dist[x]
                    while nb:
                        b = nb & -nb
                        dx[b.bit_length() - 1] = k
                        nb ^= b
        for i in range(n):
            for j in range(n):
                d = dist[i][j]
                if d >= 0:
                    val = 2 * d + p
                    if val < ans[i][j]:
                        ans[i][j] = val

    out = []
    for i in range(n):
        out.append(" ".join(str(ans[i][j]) if ans[i][j] < INF else "-1" for j in range(n)))
    sys.stdout.write("\n".join(out) + "\n")


main()
