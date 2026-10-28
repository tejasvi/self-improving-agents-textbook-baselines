import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    C = data[1:1 + n]
    # pin[v][x] = list of u with edge u->v labeled x
    pin = [dict() for _ in range(n)]
    # outm[x][v] = bitmask of w with edge v->w labeled x
    outm = {}
    edgemask = [0] * n
    for u in range(n):
        row = C[u]
        for w in range(n):
            ch = row[w]
            if ch != '-':
                pin[w].setdefault(ch, []).append(u)
                if ch not in outm:
                    outm[ch] = [0] * n
                outm[ch][u] |= 1 << w
                edgemask[u] |= 1 << w
    pin_items = [list(d.items()) for d in pin]
    # For expansion of state (u2, v2) with letter x: predecessors u in pin[u2][x],
    # and v with edge v2->v labeled x: outm[x][v2].
    # Precompute per v2 a list of (x, mask) for letters present.
    outlist = [[] for _ in range(n)]
    for x, arr in outm.items():
        for v2 in range(n):
            if arr[v2]:
                outlist[v2].append((x, arr[v2]))

    vis = [0] * n
    ans = [[-1] * n for _ in range(n)]
    pend = {}
    pend[0] = [1 << u for u in range(n)]
    pend[1] = edgemask[:]
    k = 0
    maxk = 1
    while k <= maxk:
        row = pend.pop(k, None)
        if row is None:
            k += 1
            continue
        newrows = [0] * n
        any_new = False
        for u in range(n):
            nw = row[u] & ~vis[u]
            if nw:
                vis[u] |= nw
                newrows[u] = nw
                any_new = True
                ansu = ans[u]
                m = nw
                while m:
                    low = m & -m
                    ansu[low.bit_length() - 1] = k
                    m ^= low
        if any_new:
            target = [0] * n
            for u2 in range(n):
                nw = newrows[u2]
                if not nw:
                    continue
                # for each new v2 in nw
                m = nw
                while m:
                    low = m & -m
                    v2 = low.bit_length() - 1
                    m ^= low
                    for x, Mout in outlist[v2]:
                        lst = pin[u2].get(x)
                        if lst:
                            for u in lst:
                                target[u] |= Mout
            nk = k + 2
            if nk in pend:
                pr = pend[nk]
                for u in range(n):
                    pr[u] |= target[u]
            else:
                pend[nk] = target
            if nk > maxk:
                maxk = nk
        k += 1
    out = []
    for i in range(n):
        out.append(' '.join(map(str, ans[i])))
    sys.stdout.write('\n'.join(out) + '\n')


main()
