from typing import List


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0]) if n else 0
        if n == 0 or m == 0:
            return 0

        # Directions in clockwise order: SE, SW, NW, NE.
        dirs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

        # nxt[v]: value expected after v in the pattern 1,2,0,2,0,...
        def nxt(v):
            return 2 if v != 2 else 0

        def ok_after(prev, cur):
            # Is cur a valid successor of prev in the pattern (cur not 1 except start)?
            if cur == 2:
                return prev == 1 or prev == 0
            if cur == 0:
                return prev == 2
            return False

        # P[k][i][j]: longest valid chain ending at (i,j) arriving with direction dirs[k],
        # starting with a 1. 0 if none.
        # A[k][i][j]: number of cells in the chain starting at (i,j) moving in dirs[k],
        # following the pattern from grid[i][j].
        P = []
        A = []
        for k, (dr, dc) in enumerate(dirs):
            p = [[0] * m for _ in range(n)]
            rows = range(n) if dr >= 0 else range(n - 1, -1, -1)
            cols = list(range(m)) if dc >= 0 else list(range(m - 1, -1, -1))
            for i in rows:
                pi = i - dr
                for j in cols:
                    v = grid[i][j]
                    if v == 1:
                        p[i][j] = 1
                        continue
                    pj = j - dc
                    if 0 <= pi < n and 0 <= pj < m and p[pi][pj] > 0 and ok_after(grid[pi][pj], v):
                        p[i][j] = p[pi][pj] + 1
            P.append(p)

            a = [[1] * m for _ in range(n)]
            rrows = list(rows)[::-1]
            rcols = cols[::-1]
            for i in rrows:
                ni = i + dr
                for j in rcols:
                    nj = j + dc
                    if 0 <= ni < n and 0 <= nj < m and grid[ni][nj] == nxt(grid[i][j]):
                        a[i][j] = 1 + a[ni][nj]
            A.append(a)

        best = 0
        for k in range(4):
            for i in range(n):
                for j in range(m):
                    pv = P[k][i][j]
                    if pv == 0:
                        continue
                    if pv > best:
                        best = pv
                    k2 = (k + 1) % 4
                    # Turn clockwise at (i,j): continue with direction k2 from corner.
                    total = pv + A[k2][i][j] - 1
                    if total > best:
                        best = total
        return best
