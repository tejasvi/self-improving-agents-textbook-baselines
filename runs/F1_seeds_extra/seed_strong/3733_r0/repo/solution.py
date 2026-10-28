from typing import *


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        # valid successor: 1->2, 2->0, 0->2
        nxt = [2, 2, 0]  # nxt[v]: required value after v (0->2, 1->2, 2->0)
        # clockwise order of diagonal directions
        dirs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

        # P[d][i][j]: longest chain starting with 1 that ends at (i,j) travelling in dir d
        # Q[d][i][j]: longest valid chain starting at (i,j) travelling in dir d
        P = []
        Q = []
        for di, dj in dirs:
            p = [[0] * m for _ in range(n)]
            rows = range(n) if di == 1 else range(n - 1, -1, -1)
            for i in rows:
                pi = i - di
                row = grid[i]
                prow = p[i]
                for j in range(m):
                    v = row[j]
                    if v == 1:
                        prow[j] = 1
                        continue
                    pj = j - dj
                    if 0 <= pi < n and 0 <= pj < m:
                        pv = p[pi][pj]
                        if pv and v == nxt[grid[pi][pj]]:
                            prow[j] = pv + 1
            P.append(p)
        for di, dj in dirs:
            q = [[0] * m for _ in range(n)]
            rows = range(n - 1, -1, -1) if di == 1 else range(n)
            for i in rows:
                ni = i + di
                row = grid[i]
                qrow = q[i]
                for j in range(m):
                    nj = j + dj
                    qv = 1
                    if 0 <= ni < n and 0 <= nj < m and grid[ni][nj] == nxt[row[j]]:
                        qv = q[ni][nj] + 1
                    qrow[j] = qv
            Q.append(q)

        best = 0
        for k in range(4):
            pk = P[k]
            qk = Q[(k + 1) % 4]
            for i in range(n):
                prow = pk[i]
                qrow = qk[i]
                for j in range(m):
                    a = prow[j]
                    if a:
                        t = a + qrow[j] - 1
                        if t > best:
                            best = t
        return best
