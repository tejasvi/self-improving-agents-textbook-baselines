import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    rows = data[1:1 + n]
    # inc[c][p] : list of u with edge u->p labeled c
    # Rc[c][q]  : bitmask of v with edge q->v labeled c
    inc = [[[] for _ in range(n)] for _ in range(26)]
    Rc = [[0] * n for _ in range(26)]
    edge_mask = [0] * n  # bitmask of v with edge u->v (any letter)
    for u in range(n):
        r = rows[u]
        for v in range(n):
            ch = r[v]
            if ch != '-':
                c = ord(ch) - 97
                inc[c][v].append(u)
                Rc[c][u] |= 1 << v
                edge_mask[u] |= 1 << v

    vis = [0] * n  # vis[u]: bitmask of v such that state (u,v) is finalized/queued
    ans = [[-1] * n for _ in range(n)]
    maxlev = 2 * n * n + 4
    buckets = [[] for _ in range(maxlev + 3)]

    # initial terminals
    for u in range(n):
        vis[u] |= 1 << u
        buckets[0].append((u, u))
    for u in range(n):
        m = edge_mask[u] & ~vis[u]
        vis[u] |= m
        while m:
            low = m & -m
            v = low.bit_length() - 1
            m ^= low
            buckets[1].append((u, v))

    for d in range(maxlev + 1):
        cur = buckets[d]
        if not cur:
            continue
        nxt = buckets[d + 2] if d + 2 < len(buckets) else None
        for (p, q) in cur:
            ans[p][q] = d
            if nxt is None:
                continue
            for c in range(26):
                R = Rc[c][q]
                if not R:
                    continue
                for u in inc[c][p]:
                    new = R & ~vis[u]
                    if new:
                        vis[u] |= new
                        while new:
                            low = new & -new
                            v = low.bit_length() - 1
                            new ^= low
                            nxt.append((u, v))

    sys.stdout.write("\n".join(" ".join(map(str, row)) for row in ans) + "\n")


main()
