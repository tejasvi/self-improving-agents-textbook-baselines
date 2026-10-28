from typing import *


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        # clockwise order of diagonal directions
        dirs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        best = 0
        # F[k][i][j]: length of valid arm 1,2,0,2,... moving in dirs[k], ending at (i,j)
        F = []
        # R2/R0[k][i][j]: length of alternating run starting at (i,j) in dirs[k],
        # with first value 2 / 0 respectively
        R2 = []
        R0 = []
        for k, (di, dj) in enumerate(dirs):
            f = [[0] * m for _ in range(n)]
            ii = range(n) if di == 1 else range(n - 1, -1, -1)
            jj = list(range(m)) if dj == 1 else list(range(m - 1, -1, -1))
            # forward pass: predecessor (i-di, j-dj) processed first
            for i in ii:
                pi = i - di
                fi = f[i]
                gi = grid[i]
                for j in jj:
                    v = gi[j]
                    if v == 1:
                        fi[j] = 1
                        continue
                    pj = j - dj
                    if 0 <= pi < n and 0 <= pj < m:
                        pv = grid[pi][pj]
                        pf = f[pi][pj]
                        if pf and ((v == 2 and pv != 2) or (v == 0 and pv == 2)):
                            fi[j] = pf + 1
            F.append(f)
            # backward pass for R: successor processed first
            r2 = [[0] * m for _ in range(n)]
            r0 = [[0] * m for _ in range(n)]
            rii = list(ii)[::-1]
            rjj = jj[::-1]
            for i in rii:
                ni = i + di
                for j in rjj:
                    v = grid[i][j]
                    nj = j + dj
                    if v == 2 or v == 0:
                        if 0 <= ni < n and 0 <= nj < m:
                            if v == 2:
                                r2[i][j] = 1 + r0[ni][nj]
                            else:
                                r0[i][j] = 1 + r2[ni][nj]
                        else:
                            if v == 2:
                                r2[i][j] = 1
                            else:
                                r0[i][j] = 1
            R2.append(r2)
            R0.append(r0)
        for k in range(4):
            fk = F[k]
            d2 = (k + 1) % 4
            di, dj = dirs[d2]
            r2 = R2[d2]
            r0 = R0[d2]
            for i in range(n):
                for j in range(m):
                    f1 = fk[i][j]
                    if not f1:
                        continue
                    if f1 > best:
                        best = f1
                    x = i + di
                    y = j + dj
                    if 0 <= x < n and 0 <= y < m:
                        # next index is f1; odd -> needs 2, even -> needs 0
                        t = r2[x][y] if f1 & 1 else r0[x][y]
                        if f1 + t > best:
                            best = f1 + t
        return best
