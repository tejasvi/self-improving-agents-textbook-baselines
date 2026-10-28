import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    C = data[1:1 + n]
    # inlist[w] = list of (c, u) with edge u->w labeled c
    inlist = [[] for _ in range(n)]
    # outmask[c][x] = bitmask of v with edge x->v labeled c
    outmask = {}
    for u in range(n):
        row = C[u]
        for w in range(n):
            ch = row[w]
            if ch != '-':
                inlist[w].append((ch, u))
                if ch not in outmask:
                    outmask[ch] = [0] * n
                outmask[ch][u] |= 1 << w
    INF = -1

    def bfs(sources):
        # sources: list of (u, v) with distance 0
        dist = [[-1] * n for _ in range(n)]
        vis = [0] * n
        dq = deque()
        for (u, v) in sources:
            if not (vis[u] >> v) & 1:
                vis[u] |= 1 << v
                dist[u][v] = 0
                dq.append((u, v))
        while dq:
            up, vp = dq.popleft()
            d = dist[up][vp] + 1
            for (c, u) in inlist[up]:
                m = outmask[c][vp] & ~vis[u]
                if m:
                    vis[u] |= m
                    while m:
                        low = m & -m
                        v = low.bit_length() - 1
                        dist[u][v] = d
                        dq.append((u, v))
                        m ^= low
        return dist

    even_src = [(u, u) for u in range(n)]
    odd_src = [(u, v) for u in range(n) for v in range(n) if C[u][v] != '-']
    dE = bfs(even_src)
    dO = bfs(odd_src)
    out = []
    for i in range(n):
        res = []
        for j in range(n):
            best = None
            if dE[i][j] >= 0:
                best = 2 * dE[i][j]
            if dO[i][j] >= 0:
                val = 2 * dO[i][j] + 1
                if best is None or val < best:
                    best = val
            res.append(str(best) if best is not None else "-1")
        out.append(" ".join(res))
    print("\n".join(out))

main()
