from typing import *


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        # clockwise order of diagonal directions
        D = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        nxt = {1: 2, 2: 0, 0: 2}

        # R[d][x][y]: length of valid chain starting at (x,y) moving in direction d
        R = []
        for dx, dy in D:
            r = [[1] * m for _ in range(n)]
            xs = range(n - 1, -1, -1) if dx == 1 else range(n)
            for x in xs:
                nx = x + dx
                if nx < 0 or nx >= n:
                    continue
                row = grid[x]
                nrow = grid[nx]
                rr = r[x]
                nr = r[nx]
                for y in range(m):
                    ny = y + dy
                    if 0 <= ny < m and nrow[ny] == nxt[row[y]]:
                        rr[y] = 1 + nr[ny]
            R.append(r)

        ans = 0
        for d1 in range(4):
            d2 = (d1 + 1) % 4
            dx, dy = D[d1]
            r2 = R[d2]
            r1 = R[d1]
            for x0 in range(n):
                for y0 in range(m):
                    # only start lines: previous cell out of bounds
                    px, py = x0 - dx, y0 - dy
                    if 0 <= px < n and 0 <= py < m:
                        continue
                    cells = []
                    x, y = x0, y0
                    while 0 <= x < n and 0 <= y < m:
                        cells.append((x, y))
                        x += dx
                        y += dy
                    L = len(cells)
                    M = [0] * L
                    best = -1
                    for t in range(L - 1, -1, -1):
                        cx, cy = cells[t]
                        h = t + r2[cx][cy]
                        if t + 1 < L and grid[cells[t + 1][0]][cells[t + 1][1]] == nxt[grid[cx][cy]]:
                            if M[t + 1] > h:
                                h = M[t + 1]
                        M[t] = h
                    for t in range(L):
                        cx, cy = cells[t]
                        if grid[cx][cy] == 1:
                            v = M[t] - t
                            if v > ans:
                                ans = v
                            # no-turn case
                            if r1[cx][cy] > ans:
                                ans = r1[cx][cy]
        return ans
