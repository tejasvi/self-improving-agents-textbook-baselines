from typing import *


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        W = m + 2
        size = (n + 2) * W
        val = [-1] * size
        for i in range(n):
            base = (i + 1) * W + 1
            row = grid[i]
            for j in range(m):
                val[base + j] = row[j]
        # clockwise cyclic order of diagonal directions
        dirs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        # next expected value after value v
        exp_of = [2, 2, 0]  # index by v: 0->2, 1->2, 2->0
        # F[d][t] arrays
        F = [[None, None] for _ in range(4)]
        cells_order = {}
        for d in range(4):
            di, dj = dirs[d]
            rows = range(n - 1, -1, -1) if di == 1 else range(n)
            cols = range(m - 1, -1, -1) if dj == 1 else range(m)
            # order such that next cell (i+di, j+dj) is processed before (i,j)
            order = []
            for i in rows:
                for j in cols:
                    order.append((i + 1) * W + (j + 1))
            cells_order[d] = order
        # Process t=0 for all directions first (t=1 depends on t=0 of rotated dir)
        for t in (0, 1):
            for d in range(4):
                di, dj = dirs[d]
                step = di * W + dj
                rd = (d + 1) % 4
                rstep = dirs[rd][0] * W + dirs[rd][1]
                arr = [0] * size
                F[d][t] = arr
                rarr = F[rd][0] if t == 1 else None
                for p in cells_order[d]:
                    v = val[p]
                    if v < 0:
                        continue
                    w = exp_of[v]
                    best = 1
                    q = p + step
                    if val[q] == w:
                        c = 1 + arr[q]
                        if c > best:
                            best = c
                    if t == 1:
                        q2 = p + rstep
                        if val[q2] == w:
                            c = 1 + rarr[q2]
                            if c > best:
                                best = c
                    arr[p] = best
        ans = 0
        for p in range(size):
            if val[p] == 1:
                for d in range(4):
                    if F[d][1][p] > ans:
                        ans = F[d][1][p]
        return ans
