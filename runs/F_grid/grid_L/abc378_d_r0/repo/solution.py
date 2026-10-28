import sys


def main():
    data = sys.stdin.read().split()
    H, W, K = int(data[0]), int(data[1]), int(data[2])
    grid = data[3:3 + H]
    N = H * W
    adj = [[] for _ in range(N)]
    for i in range(H):
        for j in range(W):
            if grid[i][j] != '.':
                continue
            v = i * W + j
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ni, nj = i + di, j + dj
                if 0 <= ni < H and 0 <= nj < W and grid[ni][nj] == '.':
                    adj[v].append(ni * W + nj)
    # state: (pos, visited mask) -> count
    cur = {}
    for v in range(N):
        if grid[v // W][v % W] == '.':
            cur[(v, 1 << v)] = 1
    for _ in range(K):
        nxt = {}
        get = nxt.get
        for (v, mask), c in cur.items():
            for u in adj[v]:
                bit = 1 << u
                if mask & bit:
                    continue
                key = (u, mask | bit)
                nxt[key] = get(key, 0) + c
        cur = nxt
    print(sum(cur.values()))


main()
