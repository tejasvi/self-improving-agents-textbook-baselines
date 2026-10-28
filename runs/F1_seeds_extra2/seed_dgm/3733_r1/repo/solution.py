from typing import List


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        # expected next value after a given value
        nxt = {1: 2, 2: 0, 0: 2}
        dirs = [(-1, 1), (1, 1), (1, -1), (-1, -1)]  # clockwise order
        didx = {d: k for k, d in enumerate(dirs)}

        def cw(d):
            dx, dy = d
            return (dy, -dx)

        def order(d):
            dx, dy = d
            rows = range(n - 1, -1, -1) if dx > 0 else range(n)
            cols = range(m - 1, -1, -1) if dy > 0 else range(m)
            return rows, cols

        # T0[k][i][j]: longest path starting at (i,j) moving in dirs[k], no turn allowed
        # T1[k][i][j]: same but one clockwise turn still allowed
        T0 = [[[0] * m for _ in range(n)] for _ in range(4)]
        T1 = [[[0] * m for _ in range(n)] for _ in range(4)]

        for k, d in enumerate(dirs):
            dx, dy = d
            rows, cols = order(d)
            A = T0[k]
            for i in rows:
                ri = grid[i]
                Ai = A[i]
                for j in cols:
                    need = nxt.get(ri[j])
                    if need is None:
                        continue
                    best = 0
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < n and 0 <= nj < m and grid[ni][nj] == need:
                        best = A[ni][nj]
                    Ai[j] = 1 + best

        for k, d in enumerate(dirs):
            dx, dy = d
            ck = didx[cw(d)]
            rows, cols = order(d)
            A = T1[k]
            B = T0[ck]
            for i in rows:
                ri = grid[i]
                Ai = A[i]
                for j in cols:
                    need = nxt.get(ri[j])
                    if need is None:
                        continue
                    best = 0
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < n and 0 <= nj < m and grid[ni][nj] == need:
                        best = A[ni][nj]
                    ci, cj = i + d[1], j - d[0]  # cw direction (dy, -dx)
                    if 0 <= ci < n and 0 <= cj < m and grid[ci][cj] == need:
                        best = max(best, B[ci][cj])
                    Ai[j] = 1 + best

        ans = 0
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 1:
                    for k in range(4):
                        if T1[k][i][j] > ans:
                            ans = T1[k][i][j]
        return ans
