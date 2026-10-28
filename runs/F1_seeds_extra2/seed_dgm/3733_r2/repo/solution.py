from typing import List


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        # Clockwise order of diagonal directions (row delta, col delta).
        dirs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

        def expected(v):
            # Value that must follow v in the sequence 1,2,0,2,0,...
            return 0 if v == 2 else 2

        # F[d][i][j]: longest valid run starting with a 1 and moving in
        # direction d, ending at (i, j). 0 if none.
        F = []
        # L[d][i][j]: longest valid run starting at (i, j) and moving in
        # direction d (the run's values follow the pattern from grid[i][j]).
        L = []
        for dr, dc in dirs:
            f = [[0] * m for _ in range(n)]
            rows = range(n) if dr == 1 else range(n - 1, -1, -1)
            cols = range(m) if dc == 1 else range(m - 1, -1, -1)
            for i in rows:
                pi = i - dr
                for j in cols:
                    v = grid[i][j]
                    if v == 1:
                        f[i][j] = 1
                        continue
                    pj = j - dc
                    if 0 <= pi < n and 0 <= pj < m and f[pi][pj] > 0 \
                            and expected(grid[pi][pj]) == v:
                        f[i][j] = f[pi][pj] + 1
            F.append(f)

            l = [[0] * m for _ in range(n)]
            rows = range(n - 1, -1, -1) if dr == 1 else range(n)
            cols = range(m - 1, -1, -1) if dc == 1 else range(m)
            for i in rows:
                ni = i + dr
                for j in cols:
                    v = grid[i][j]
                    if v == 1 or v == 2 or v == 0:
                        l[i][j] = 1
                    else:
                        continue
                    nj = j + dc
                    if 0 <= ni < n and 0 <= nj < m and l[ni][nj] > 0 \
                            and expected(v) == grid[ni][nj]:
                        l[i][j] = l[ni][nj] + 1
            L.append(l)

        best = 0
        for d in range(4):
            d2 = (d + 1) % 4
            f = F[d]
            l2 = L[d2]
            for i in range(n):
                for j in range(m):
                    fv = f[i][j]
                    if fv == 0:
                        continue
                    if fv > best:
                        best = fv
                    # Turn clockwise at (i, j): continue with direction d2.
                    total = fv + l2[i][j] - 1
                    if total > best:
                        best = total
        return best
