import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    rows = data[1:1 + n]
    INF = -1
    g = [[INF] * n for _ in range(n)]
    # in_c[c][w] = list of u with edge u->w labeled c
    # out_c[c][w] = bitmask of v with edge w->v labeled c
    in_c = [[[] for _ in range(n)] for _ in range(26)]
    out_c = [[0] * n for _ in range(26)]
    unvis = [(1 << n) - 1] * n  # unvis[u]: bitmask of v with g[u][v] unset
    buckets = {0: []}
    for u in range(n):
        r = rows[u]
        for v in range(n):
            ch = r[v]
            if ch != '-':
                c = ord(ch) - 97
                in_c[c][v].append(u)
                out_c[c][u] |= 1 << v
                if g[u][v] == INF and u != v:
                    g[u][v] = 1
                    unvis[u] &= ~(1 << v)
                    buckets.setdefault(1, []).append((u, v))
    for u in range(n):
        g[u][u] = 0
        unvis[u] &= ~(1 << u)
        buckets[0].append((u, u))

    # Bucket BFS over pair-states (front, back); seeds are dist 0 or 1.
    d = 0
    while buckets:
        lst = buckets.pop(d, [])
        nxt = []
        for (up, vp) in lst:
            # predecessors (u,v): edge u->up labeled c and edge vp->v labeled c
            for c in range(26):
                om = out_c[c][vp]
                if not om:
                    continue
                for u in in_c[c][up]:
                    m = om & unvis[u]
                    if m:
                        unvis[u] ^= m
                        row = g[u]
                        while m:
                            b = m & -m
                            v = b.bit_length() - 1
                            row[v] = d + 2
                            nxt.append((u, v))
                            m ^= b
        if nxt:
            buckets.setdefault(d + 2, []).extend(nxt)
        d += 1

    out = [' '.join(str(x) for x in g[i]) for i in range(n)]
    sys.stdout.write('\n'.join(out) + '\n')


main()
