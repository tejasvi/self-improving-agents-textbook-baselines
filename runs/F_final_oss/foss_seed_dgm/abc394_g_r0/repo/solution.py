# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    import sys
    sys.setrecursionlimit(1 << 25)
    input = sys.stdin.readline
    line = input().split()
    if not line:
        return
    H, W = map(int, line)
    N = H * W
    heights = []  # list of (height, idx)
    grid = []
    max_h = 0
    for i in range(H):
        row = list(map(int, input().split()))
        grid.append(row)
        for j, h in enumerate(row):
            idx = i * W + j
            heights.append((h, idx))
            if h > max_h:
                max_h = h
    Q = int(input())
    start_idx = [0] * Q
    target_idx = [0] * Q
    Y = [0] * Q
    Z = [0] * Q
    for qi in range(Q):
        a, b, y, c, d, z = map(int, input().split())
        a -= 1; b -= 1; c -= 1; d -= 1
        start_idx[qi] = a * W + b
        target_idx[qi] = c * W + d
        Y[qi] = y
        Z[qi] = z

    class DSU:
        __slots__ = ('parent', 'size')
        def __init__(self, n):
            self.parent = list(range(n))
            self.size = [1] * n
        def find(self, x):
            while self.parent[x] != x:
                self.parent[x] = self.parent[self.parent[x]]
                x = self.parent[x]
            return x
        def union(self, a, b):
            ra = self.find(a)
            rb = self.find(b)
            if ra == rb:
                return
            if self.size[ra] < self.size[rb]:
                ra, rb = rb, ra
            self.parent[rb] = ra
            self.size[ra] += self.size[rb]

    # Sort cells by height descending
    heights.sort(reverse=True)

    # Parallel binary search to find max floor M such that start and target are connected via cells with height >= M
    lo = [0] * Q  # inclusive, connected at lo
    hi = [max_h + 1] * Q  # exclusive, not connected at hi
    while True:
        buckets = {}
        any_pending = False
        for i in range(Q):
            if lo[i] + 1 < hi[i]:
                any_pending = True
                mid = (lo[i] + hi[i]) // 2
                buckets.setdefault(mid, []).append(i)
        if not any_pending:
            break
        mids_desc = sorted(buckets.keys(), reverse=True)
        dsu = DSU(N)
        added = [False] * N
        ptr = 0
        for cur_mid in mids_desc:
            while ptr < N and heights[ptr][0] >= cur_mid:
                h, idx = heights[ptr]
                added[idx] = True
                i = idx // W
                j = idx % W
                if i > 0:
                    nb = (i - 1) * W + j
                    if added[nb]:
                        dsu.union(idx, nb)
                if i + 1 < H:
                    nb = (i + 1) * W + j
                    if added[nb]:
                        dsu.union(idx, nb)
                if j > 0:
                    nb = i * W + (j - 1)
                    if added[nb]:
                        dsu.union(idx, nb)
                if j + 1 < W:
                    nb = i * W + (j + 1)
                    if added[nb]:
                        dsu.union(idx, nb)
                ptr += 1
            for qi in buckets[cur_mid]:
                if dsu.find(start_idx[qi]) == dsu.find(target_idx[qi]):
                    lo[qi] = cur_mid
                else:
                    hi[qi] = cur_mid
    # Now lo[i] = maximum floor M where start and target are connected via cells with height >= M
    out = []
    for i in range(Q):
        M = lo[i]
        y = Y[i]
        z = Z[i]
        low = y if y < z else z
        high = z if y < z else y
        if low <= M <= high:
            ans = high - low
        elif M < low:
            ans = y + z - 2 * M
        else:  # M > high
            ans = 2 * M - y - z
        out.append(str(ans))
    sys.stdout.write('\n'.join(out))

if __name__ == "__main__":
    solve()
