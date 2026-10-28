import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    H, W, T = int(data[0]), int(data[1]), int(data[2])
    rows = data[3:3 + H]
    Wp = W + 2
    wall = [True] * ((H + 2) * Wp)
    S = G = -1
    candies = []
    for i in range(H):
        r = rows[i]
        base = (i + 1) * Wp + 1
        for j in range(W):
            c = r[j]
            p = base + j
            if c == '#':
                continue
            wall[p] = False
            if c == 'S':
                S = p
            elif c == 'G':
                G = p
            elif c == 'o':
                candies.append(p)
    INF = 10 ** 15

    def bfs(src):
        dist = [-1] * len(wall)
        dist[src] = 0
        dq = deque([src])
        pop = dq.popleft
        push = dq.append
        while dq:
            p = pop()
            nd = dist[p] + 1
            for q in (p - 1, p + 1, p - Wp, p + Wp):
                if not wall[q] and dist[q] < 0:
                    dist[q] = nd
                    push(q)
        return dist

    def get(d, p):
        return d[p] if d[p] >= 0 else INF

    dS = bfs(S)
    if get(dS, G) > T:
        print(-1)
        return
    n = len(candies)
    if n == 0:
        print(0)
        return
    cd = [bfs(c) for c in candies]
    # D[v][u]: distance between candies; dG[v]: candy v to goal; s[u]: S to candy u
    D = [[get(cd[v], candies[u]) for u in range(n)] for v in range(n)]
    dG = [get(cd[v], G) for v in range(n)]
    s = [get(dS, candies[u]) for u in range(n)]
    best = 0
    try:
        import numpy as np
        FULL = 1 << n
        dp = np.full((FULL, n), INF, dtype=np.int64)
        for u in range(n):
            dp[1 << u, u] = s[u]
        Dn = np.array(D, dtype=np.int64)  # Dn[v][u]
        masks = np.arange(FULL, dtype=np.int64)
        pc = np.zeros(FULL, dtype=np.int64)
        for b in range(n):
            pc += (masks >> b) & 1
        dGn = np.array(dG, dtype=np.int64)
        Tn = T
        for k in range(1, n + 1):
            layer = masks[pc == k]
            if k < n:
                for u in range(n):
                    M = layer[((layer >> u) & 1) == 0]
                    if M.size == 0:
                        continue
                    vals = (dp[M] + Dn[:, u][None, :]).min(axis=1)
                    vals = np.minimum(vals, INF)
                    tgt = M | (1 << u)
                    dp[tgt, u] = np.minimum(dp[tgt, u], vals)
            # check completion for layer k
            L = dp[layer]
            tot = L + dGn[None, :]
            ok = (tot <= Tn).any(axis=1)
            if ok.any():
                best = k
        print(best)
        return
    except ImportError:
        pass
    # pure-Python fallback
    FULL = 1 << n
    dp = [[INF] * n for _ in range(FULL)]
    for u in range(n):
        dp[1 << u][u] = s[u]
    for mask in range(1, FULL):
        row = dp[mask]
        for v in range(n):
            cur = row[v]
            if cur > T:
                continue
            if cur + dG[v] <= T:
                k = bin(mask).count('1')
                if k > best:
                    best = k
            Dv = D[v]
            for u in range(n):
                if mask >> u & 1:
                    continue
                nv = cur + Dv[u]
                if nv < dp[mask | (1 << u)][u]:
                    dp[mask | (1 << u)][u] = nv
    print(best)

main()
