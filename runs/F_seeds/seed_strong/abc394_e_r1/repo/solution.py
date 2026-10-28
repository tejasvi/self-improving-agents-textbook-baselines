import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    rows = data[1:1 + N]
    # inl[x] = list of (u, c): edge u -> x labeled c
    # outm[c][x] = bitmask of v such that edge x -> v labeled c
    inl = [[] for _ in range(N)]
    outm = [[0] * N for _ in range(26)]
    E = [0] * N  # E[u] = bitmask of v with any edge u->v
    for i in range(N):
        r = rows[i]
        for j in range(N):
            ch = r[j]
            if ch != '-':
                c = ord(ch) - 97
                inl[j].append((i, c))
                outm[c][i] |= 1 << j
                E[i] |= 1 << j

    def bfs(sources):
        # sources: list of (u, v) terminal states at distance 0
        dist = [[-1] * N for _ in range(N)]
        vis = [0] * N
        q = deque()
        for u, v in sources:
            if not (vis[u] >> v) & 1:
                vis[u] |= 1 << v
                dist[u][v] = 0
                q.append((u, v))
        while q:
            up, vp = q.popleft()
            d = dist[up][vp] + 1
            for u, c in inl[up]:
                m = outm[c][vp] & ~vis[u]
                if m:
                    vis[u] |= m
                    while m:
                        low = m & -m
                        v = low.bit_length() - 1
                        dist[u][v] = d
                        q.append((u, v))
                        m ^= low
        return dist

    dE = bfs([(u, u) for u in range(N)])
    dO = bfs([(u, v) for u in range(N) for v in range(N) if (E[u] >> v) & 1])
    out = []
    for i in range(N):
        row = []
        for j in range(N):
            best = -1
            if dE[i][j] >= 0:
                best = 2 * dE[i][j]
            if dO[i][j] >= 0:
                cand = 2 * dO[i][j] + 1
                if best < 0 or cand < best:
                    best = cand
            row.append(str(best))
        out.append(" ".join(row))
    sys.stdout.write("\n".join(out) + "\n")


main()
