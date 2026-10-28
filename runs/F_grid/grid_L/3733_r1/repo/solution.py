from typing import List


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        # Directions in clockwise order: SE, SW, NW, NE
        dirs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        # successor in the sequence 1,2,0,2,0,...
        succ = {1: 2, 2: 0, 0: 2}

        # A[d][i][j]: longest valid chain (starting with 1) ending at (i,j),
        # whose last step moved in direction d (arriving at (i,j)).
        A = []
        # B[d][i][j]: longest valid chain starting at (i,j) moving in direction d.
        B = []
        for dr, dc in dirs:
            a = [[0] * m for _ in range(n)]
            rows = range(n) if dr == 1 else range(n - 1, -1, -1)
            cols = range(m) if dc == 1 else range(m - 1, -1, -1)
            for i in rows:
                pi = i - dr
                ai = a[i]
                gi = grid[i]
                for j in cols:
                    v = gi[j]
                    if v == 1:
                        ai[j] = 1
                        continue
                    pj = j - dc
                    if 0 <= pi < n and 0 <= pj < m:
                        pv = a[pi][pj]
                        if pv and succ[grid[pi][pj]] == v:
                            ai[j] = pv + 1
            A.append(a)

            b = [[1] * m for _ in range(n)]
            rows = range(n - 1, -1, -1) if dr == 1 else range(n)
            cols = range(m - 1, -1, -1) if dc == 1 else range(m)
            for i in rows:
                ni = i + dr
                gi = grid[i]
                bi = b[i]
                for j in cols:
                    nj = j + dc
                    if 0 <= ni < n and 0 <= nj < m and succ[gi[j]] == grid[ni][nj]:
                        bi[j] = b[ni][nj] + 1
            B.append(b)

        best = 0
        for i in range(n):
            for j in range(m):
                for d in range(4):
                    av = A[d][i][j]
                    if av == 0:
                        continue
                    if av > best:
                        best = av
                    cand = av + B[(d + 1) % 4][i][j] - 1
                    if cand > best:
                        best = cand
        return best
