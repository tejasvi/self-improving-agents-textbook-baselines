from typing import *


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        M = m + 2
        N = n + 2
        val = [-1] * (N * M)
        for i in range(n):
            base = (i + 1) * M + 1
            row = grid[i]
            for j in range(m):
                val[base + j] = row[j]
        # next required value after v: 1->2, 2->0, 0->2
        nx = {0: 2, 1: 2, 2: 0}
        dirs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]  # clockwise order
        # t0[d]: straight-only; t1[d]: one turn still available
        t0 = [None] * 4
        t1 = [None] * 4
        for d in range(4):
            t0[d] = [0] * (N * M)
        # Compute t0 for all directions first
        for d in range(4):
            di, dj = dirs[d]
            off = di * M + dj
            g = t0[d]
            rows = range(n, 0, -1) if di == 1 else range(1, n + 1)
            cols = range(m, 0, -1) if dj == 1 else range(1, m + 1)
            for i in rows:
                base = i * M
                for j in cols:
                    p = base + j
                    q = p + off
                    if val[q] == nx[val[p]]:
                        g[p] = 1 + g[q]
                    else:
                        g[p] = 1
        # Compute t1 for all directions
        for d in range(4):
            t1[d] = [0] * (N * M)
        for d in range(4):
            di, dj = dirs[d]
            off = di * M + dj
            cd = (d + 1) % 4
            coff = dirs[cd][0] * M + dirs[cd][1]
            g1 = t1[d]
            g0c = t0[cd]
            rows = range(n, 0, -1) if di == 1 else range(1, n + 1)
            cols = range(m, 0, -1) if dj == 1 else range(1, m + 1)
            for i in rows:
                base = i * M
                for j in cols:
                    p = base + j
                    need = nx[val[p]]
                    best = 0
                    q = p + off
                    if val[q] == need:
                        best = g1[q]
                    q2 = p + coff
                    if val[q2] == need:
                        if g0c[q2] > best:
                            best = g0c[q2]
                    g1[p] = 1 + best
        ans = 0
        for i in range(1, n + 1):
            base = i * M
            for j in range(1, m + 1):
                p = base + j
                if val[p] == 1:
                    for d in range(4):
                        if t1[d][p] > ans:
                            ans = t1[d][p]
        return ans
