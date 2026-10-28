import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    C = data[1:1 + n]
    # outm[v][c] : bitmask of w with edge v->w labeled c
    # inl[u'][c] : list of u with edge u->u' labeled c
    outm = [dict() for _ in range(n)]
    inl = [dict() for _ in range(n)]
    for x in range(n):
        row = C[x]
        for y in range(n):
            ch = row[y]
            if ch != '-':
                outm[x][ch] = outm[x].get(ch, 0) | (1 << y)
                inl[y].setdefault(ch, []).append(x)

    INF = -1
    ans = [[INF] * n for _ in range(n)]
    visited = [0] * n
    # Level 0 initial: (x, x)
    init0 = [1 << x for x in range(n)]
    # Level 1 initial: (x, y) with edge x->y
    init1 = [0] * n
    for x in range(n):
        m = 0
        for ch, mk in outm[x].items():
            m |= mk
        init1[x] = m

    prev2 = [0] * n  # frontier at d-2
    prev1 = [0] * n  # frontier at d-1
    d = 0
    while True:
        cur_init = init0 if d == 0 else (init1 if d == 1 else None)
        # Step: from frontier at d-2
        new = [0] * n
        if d >= 2:
            # G[c][u'] = OR over v' in prev2[u'] of outm[v'][c]
            G = {}
            for up in range(n):
                m = prev2[up]
                while m:
                    low = m & -m
                    vp = low.bit_length() - 1
                    m ^= low
                    for ch, mk in outm[vp].items():
                        g = G.get(ch)
                        if g is None:
                            g = [0] * n
                            G[ch] = g
                        g[up] |= mk
            for ch, g in G.items():
                for up in range(n):
                    gv = g[up]
                    if gv:
                        for u in inl[up].get(ch, ()):
                            new[u] |= gv
        cur = [0] * n
        for u in range(n):
            m = new[u]
            if cur_init is not None:
                m |= cur_init[u]
            m &= ~visited[u]
            cur[u] = m
            if m:
                visited[u] |= m
                mm = m
                while mm:
                    low = mm & -mm
                    j = low.bit_length() - 1
                    mm ^= low
                    ans[u][j] = d
        # termination check
        if d >= 1 and not any(cur) and not any(prev1):
            break
        prev2, prev1 = prev1, cur
        d += 1
    out = []
    for i in range(n):
        out.append(' '.join(str(x) for x in ans[i]))
    sys.stdout.write('\n'.join(out) + '\n')


main()
