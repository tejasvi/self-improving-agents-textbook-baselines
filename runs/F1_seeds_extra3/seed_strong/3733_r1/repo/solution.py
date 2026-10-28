from typing import *


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        # padded grid: border value -1 (invalid)
        W = m + 2
        g_val = [-1] * ((n + 2) * W)
        for i in range(n):
            base = (i + 1) * W + 1
            row = grid[i]
            for j in range(m):
                g_val[base + j] = row[j]
        # expected next value after v: 1->2, 2->0, 0->2
        nxt = {1: 2, 2: 0, 0: 2}

        # directions in clockwise order (screen coords, row dr, col dc)
        dirs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        N = (n + 2) * W
        offs = [dr * W + dc for dr, dc in dirs]

        # F[k][idx]: length of alternating run from a 1, ending at idx, moving in dirs[k]
        F = [None] * 4
        G = [None] * 4
        for k, (dr, dc) in enumerate(dirs):
            off = offs[k]
            f = [0] * N
            # iterate so that predecessor (idx - off) is processed earlier
            rows = range(1, n + 1) if dr == 1 else range(n, 0, -1)
            cols = range(1, m + 1) if dc == 1 else range(m, 0, -1)
            for i in rows:
                base = i * W
                for j in cols:
                    idx = base + j
                    v = g_val[idx]
                    if v == 1:
                        f[idx] = 1
                    elif v == 0 or v == 2:
                        p = idx - off
                        pv = g_val[p]
                        if pv >= 0 and nxt[pv] == v and f[p] > 0:
                            f[idx] = f[p] + 1
            F[k] = f

            gg = [0] * N
            # g depends on successor idx + off: iterate in reverse order
            rows_r = range(n, 0, -1) if dr == 1 else range(1, n + 1)
            cols_r = range(m, 0, -1) if dc == 1 else range(1, m + 1)
            for i in rows_r:
                base = i * W
                for j in cols_r:
                    idx = base + j
                    v = g_val[idx]
                    if v == 0 or v == 1 or v == 2:
                        s = idx + off
                        if g_val[s] == nxt[v]:
                            gg[idx] = 1 + gg[s]
                        else:
                            gg[idx] = 1
            G[k] = gg

        best = 0
        for k in range(4):
            f = F[k]
            mx = max(f)
            if mx > best:
                best = mx
        for k in range(4):
            f = F[k]
            k2 = (k + 1) % 4  # clockwise turn
            gg = G[k2]
            off2 = offs[k2]
            for i in range(1, n + 1):
                base = i * W
                for j in range(1, m + 1):
                    idx = base + j
                    fv = f[idx]
                    if fv == 0:
                        continue
                    s = idx + off2
                    # second leg starts at s, must match expected of corner
                    if g_val[s] == nxt[g_val[idx]]:
                        tot = fv + gg[s]
                        if tot > best:
                            best = tot
        return best
