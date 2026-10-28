from typing import *

# Directions in clockwise order (screen coordinates: row down, col right).
_DIRS = [(1, 1), (1, -1), (-1, -1), (-1, 1)]


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        # Padded grid: value -1 outside the matrix (never matches).
        P = [[-1] * (m + 2) for _ in range(n + 2)]
        for i in range(n):
            P[i + 1][1:m + 1] = grid[i]

        # nxt(v): required value after v in the sequence 1,2,0,2,0,...
        def nxt(v):
            if v == 1:
                return 2
            if v == 2:
                return 0
            if v == 0:
                return 2
            return -2  # never matches

        R = range(1, n + 1)
        C = range(1, m + 1)
        rows_asc = list(R)
        rows_desc = rows_asc[::-1]
        cols_asc = list(C)
        cols_desc = cols_asc[::-1]

        # B[d][i][j]: length of valid straight path ending at (i,j) moving in dir d,
        # starting with a 1 at the path start.
        # F[d][i][j]: length of maximal chain starting at (i,j) moving in dir d
        # (following nxt), including (i,j).
        B = []
        F = []
        for d, (dr, dc) in enumerate(_DIRS):
            Bd = [[0] * (m + 2) for _ in range(n + 2)]
            Fd = [[0] * (m + 2) for _ in range(n + 2)]
            rows_b = rows_asc if dr == 1 else rows_desc
            cols_b = cols_asc if dc == 1 else cols_desc
            # Process so that predecessor (i-dr, j-dc) is computed first.
            for i in rows_b:
                Pi = P[i]
                Bi = Bd[i]
                Bp = Bd[i - dr]
                for j in cols_b:
                    v = Pi[j]
                    if v == 1:
                        Bi[j] = 1
                    elif v == 0 or v == 2:
                        pv = P[i - dr][j - dc]
                        if pv >= 0 and Bp[j - dc] and nxt(pv) == v:
                            Bi[j] = Bp[j - dc] + 1
            # F: process in reverse order so successor is computed first.
            rows_f = rows_desc if dr == 1 else rows_asc
            cols_f = cols_desc if dc == 1 else cols_asc
            for i in rows_f:
                Pi = P[i]
                Fi = Fd[i]
                for j in cols_f:
                    v = Pi[j]
                    if v < 0:
                        continue
                    f = 1
                    sv = P[i + dr][j + dc]
                    if sv >= 0 and sv == nxt(v):
                        f += Fd[i + dr][j + dc]
                    Fi[j] = f
            B.append(Bd)
            F.append(Fd)

        best = 0
        for d in range(4):
            Bd = B[d]
            d2 = (d + 1) % 4
            dr2, dc2 = _DIRS[d2]
            F2 = F[d2]
            for i in R:
                Pi = P[i]
                Bi = Bd[i]
                for j in C:
                    b = Bi[j]
                    if b == 0:
                        continue
                    total = b
                    v = Pi[j]
                    ni, nj = i + dr2, j + dc2
                    if P[ni][nj] == nxt(v) and P[ni][nj] >= 0:
                        total = b + F2[ni][nj]
                    if total > best:
                        best = total
        return best
