import sys
from collections import deque
from operator import add


def main():
    data = sys.stdin.read().split()
    H, W, T = int(data[0]), int(data[1]), int(data[2])
    grid = "".join(data[3:3 + H])
    N = H * W
    S = G = -1
    candies = []
    for idx, ch in enumerate(grid):
        if ch == 'S':
            S = idx
        elif ch == 'G':
            G = idx
        elif ch == 'o':
            candies.append(idx)
    n = len(candies)
    wall = [ch == '#' for ch in grid]
    BIG = 10 ** 18

    def bfs(src):
        dist = [-1] * N
        dist[src] = 0
        dq = deque([src])
        pop = dq.popleft
        push = dq.append
        while dq:
            v = pop()
            d = dist[v] + 1
            r, c = divmod(v, W)
            if r > 0:
                u = v - W
                if dist[u] < 0 and not wall[u]:
                    dist[u] = d; push(u)
            if r < H - 1:
                u = v + W
                if dist[u] < 0 and not wall[u]:
                    dist[u] = d; push(u)
            if c > 0:
                u = v - 1
                if dist[u] < 0 and not wall[u]:
                    dist[u] = d; push(u)
            if c < W - 1:
                u = v + 1
                if dist[u] < 0 and not wall[u]:
                    dist[u] = d; push(u)
        return dist

    def conv(d):
        return BIG if d < 0 else d

    dS_full = bfs(S)
    if dS_full[G] < 0 or dS_full[G] > T:
        print(-1)
        return

    dG_full = bfs(G)
    dS = [conv(dS_full[c]) for c in candies]
    dG = [conv(dG_full[c]) for c in candies]
    # D[v][u]: distance between candy v and candy u (symmetric)
    D = []
    for c in candies:
        dist = bfs(c)
        D.append([conv(dist[c2]) for c2 in candies])

    # dp[mask][v]: min moves from S, visiting exactly candies in mask, ending at candy v
    # (only values <= T are kept; others are BIG)
    full = 1 << n
    dp = [None] * full
    for u in range(n):
        if dS[u] <= T:
            row = [BIG] * n
            row[u] = dS[u]
            dp[1 << u] = row

    ans = 0
    if dS_full[G] <= T:
        ans = 0
    for mask in range(1, full):
        row = dp[mask]
        if row is None:
            continue
        pc = bin(mask).count('1')
        if pc > ans and min(map(add, row, dG)) <= T:
            ans = pc
        for u in range(n):
            bit = 1 << u
            if mask & bit:
                continue
            cand = min(map(add, row, D[u]))
            if cand > T:
                continue
            nm = mask | bit
            nrow = dp[nm]
            if nrow is None:
                nrow = [BIG] * n
                dp[nm] = nrow
            if cand < nrow[u]:
                nrow[u] = cand
    print(ans)


main()
