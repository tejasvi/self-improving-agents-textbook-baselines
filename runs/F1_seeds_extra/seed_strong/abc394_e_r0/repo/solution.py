import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    rows = data[1:1 + n]
    # outedges[i] = list of (u, c) with edge i->u labeled c
    outedges = [[] for _ in range(n)]
    # OutC[c][v] = bitmask of j with edge v->j labeled c
    OutC = [[0] * n for _ in range(26)]
    for i in range(n):
        r = rows[i]
        for j in range(n):
            ch = r[j]
            if ch != '-':
                c = ord(ch) - 97
                outedges[i].append((j, c))
                OutC[c][i] |= 1 << j
    val = [[-1] * n for _ in range(n)]
    settled = [0] * n
    prev = {}  # level -> list of frontier rows (bitmask over v per u)
    base1 = [0] * n
    for i in range(n):
        for (j, c) in outedges[i]:
            if j != i:
                base1[i] |= 1 << j
    base0 = [1 << i for i in range(n)]
    S = {}
    empty_run = 0
    d = 0
    LIMIT = 2 * n * n + 10
    while d <= LIMIT:
        if d == 0:
            new = base0[:]
        elif d == 1:
            new = base1[:]
        else:
            F = S.get(d - 2)
            new = [0] * n
            if F is not None and any(F):
                # H[u][c] = bitmask of j such that exists v in F[u] with edge v->j labeled c
                H = [None] * n
                for u in range(n):
                    fu = F[u]
                    if not fu:
                        continue
                    h = [0] * 26
                    v = 0
                    while fu:
                        if fu & 1:
                            for c in range(26):
                                h[c] |= OutC[c][v]
                        fu >>= 1
                        v += 1
                    H[u] = h
                for i in range(n):
                    acc = 0
                    for (u, c) in outedges[i]:
                        hu = H[u]
                        if hu is not None:
                            acc |= hu[c]
                    new[i] = acc
        cur = [0] * n
        any_new = False
        for i in range(n):
            x = new[i] & ~settled[i]
            if x:
                any_new = True
                cur[i] = x
                settled[i] |= x
                vi = val[i]
                while x:
                    lb = x & -x
                    vi[lb.bit_length() - 1] = d
                    x ^= lb
        S[d] = cur
        if any_new:
            empty_run = 0
        else:
            empty_run += 1
            if empty_run >= 2:
                break
        d += 1
    sys.stdout.write('\n'.join(' '.join(map(str, row)) for row in val) + '\n')

main()
