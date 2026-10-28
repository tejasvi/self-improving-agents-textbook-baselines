import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    rows = data[1:1 + n]

    # inl[v] = list of (u, c) with edge u->v labeled c
    inl = [[] for _ in range(n)]
    # outmask[v][c] = bitmask of w such that edge v->w labeled c
    outmask = [dict() for _ in range(n)]
    adj_out = [[] for _ in range(n)]
    for u in range(n):
        r = rows[u]
        for v in range(n):
            ch = r[v]
            if ch != '-':
                inl[v].append((u, ch))
                outmask[u][ch] = outmask[u].get(ch, 0) | (1 << v)
                adj_out[u].append(v)

    INF = -1
    maxc = 2 * n * n + 5
    buckets = [[] for _ in range(maxc)]
    seen = [0] * n  # bitmask per row u of seen states (u, v)
    dist = [[-1] * n for _ in range(n)]

    # Terminal seeds
    for u in range(n):
        seen[u] |= 1 << u
        buckets[0].append((u, u))
    for u in range(n):
        for v in adj_out[u]:
            if not (seen[u] >> v) & 1:
                seen[u] |= 1 << v
                buckets[1].append((u, v))

    for d in range(maxc):
        bk = buckets[d]
        if not bk:
            continue
        nd = d + 2
        for (u2, v2) in bk:
            dist[u2][v2] = d
            if nd >= maxc:
                continue
            # predecessors (u, v): u in in(u2) with label c, v in out(v2) with label c
            om = outmask[v2]
            for (u, c) in inl[u2]:
                m = om.get(c, 0)
                if not m:
                    continue
                new = m & ~seen[u]
                if new:
                    seen[u] |= new
                    bb = buckets[nd]
                    while new:
                        b = new & -new
                        bb.append((u, b.bit_length() - 1))
                        new ^= b
        buckets[d] = None

    out = []
    for i in range(n):
        out.append(' '.join(str(x) for x in dist[i]))
    sys.stdout.write('\n'.join(out) + '\n')


main()
