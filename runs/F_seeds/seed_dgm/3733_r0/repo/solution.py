from typing import List


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        # Directions in clockwise order: SE, SW, NW, NE
        dirs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

        def valid(cur, nxt):
            # after 1 or 0 comes 2; after 2 comes 0
            if cur == 2:
                return nxt == 0
            return nxt == 2

        # B[d][i][j]: longest valid chain ending at (i,j) moving in dir d, starting with a 1
        B = [[[0] * m for _ in range(n)] for _ in range(4)]
        # S[d][i][j]: longest valid chain starting at (i,j) moving in dir d
        S = [[[0] * m for _ in range(n)] for _ in range(4)]

        for d, (dr, dc) in enumerate(dirs):
            Bd = B[d]
            # predecessor (i-dr, j-dc) must be processed first: rows ascending if dr=1
            rows = range(n) if dr == 1 else range(n - 1, -1, -1)
            for i in rows:
                pi = i - dr
                for j in range(m):
                    v = grid[i][j]
                    if v == 1:
                        Bd[i][j] = 1
                        continue
                    pj = j - dc
                    if 0 <= pi < n and 0 <= pj < m:
                        pb = Bd[pi][pj]
                        if pb > 0 and valid(grid[pi][pj], v):
                            Bd[i][j] = pb + 1

        for d, (dr, dc) in enumerate(dirs):
            Sd = S[d]
            # successor (i+dr, j+dc) must be processed first: rows descending if dr=1
            rows = range(n - 1, -1, -1) if dr == 1 else range(n)
            for i in rows:
                ni = i + dr
                for j in range(m):
                    v = grid[i][j]
                    Sd[i][j] = 1
                    nj = j + dc
                    if 0 <= ni < n and 0 <= nj < m and valid(v, grid[ni][nj]):
                        Sd[i][j] = Sd[ni][nj] + 1

        best = 0
        for d in range(4):
            Bd = B[d]
            for i in range(n):
                for j in range(m):
                    b = Bd[i][j]
                    if b == 0:
                        continue
                    if b > best:
                        best = b
                    # turn clockwise at (i,j): incoming d, outgoing (d+1)%4
                    s = S[(d + 1) % 4][i][j]
                    if s > 0 and b + s - 1 > best:
                        best = b + s - 1
        return best
