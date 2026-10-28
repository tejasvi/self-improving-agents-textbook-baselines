from typing import *


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        # padded grid: value -1 outside
        g = [[-1] * (m + 2) for _ in range(n + 2)]
        for i in range(n):
            row = grid[i]
            gi = g[i + 1]
            for j in range(m):
                gi[j + 1] = row[j]
        # clockwise order of diagonal directions (screen coords)
        dirs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

        # R[d][s][x][y]: length of alternating run starting at (x,y) in dir d
        # whose first expected value is s (s in {0,2}), counting cells with
        # values s, other(s), s, ...
        R = []
        for (dx, dy) in dirs:
            Rd = {}
            for s in (0, 2):
                Rd[s] = [[0] * (m + 2) for _ in range(n + 2)]
            # dependency (x+dx, y+dy): process rows so that x+dx is done first
            rows = range(n, 0, -1) if dx == 1 else range(1, n + 1)
            for x in rows:
                for s in (0, 2):
                    other = 2 - s
                    cur = Rd[s][x]
                    nxt = Rd[other][x + dx]
                    gx = g[x]
                    for y in range(1, m + 1):
                        if gx[y] == s:
                            cur[y] = 1 + nxt[y + dy]
                    # note: within a row, dependencies are on other rows only
                # cells in row x depend on row x+dx only (dx != 0)
            R.append(Rd)

        ans = 0
        for d in range(4):
            dx, dy = dirs[d]
            nd = (d + 1) % 4
            ddx, ddy = dirs[nd]
            Rn = R[nd]
            # Lg: chain ending at p in direction d; depends on p-d
            Lg = [[0] * (m + 2) for _ in range(n + 2)]
            rows = range(1, n + 1) if dx == 1 else range(n, 0, -1)
            for x in rows:
                px = x - dx
                gx = g[x]
                Lx = Lg[x]
                Lprev = Lg[px]
                for y in range(1, m + 1):
                    v = gx[y]
                    if v == 1:
                        Lx[y] = 1
                        continue
                    k = Lprev[y - dy]
                    if k and v == (2 if k % 2 == 1 else 0):
                        Lx[y] = k + 1
                        # candidate: straight ends here
                        t = k + 1
                        if t > ans:
                            ans = t
                        # turn clockwise at this cell
                        qx = x + ddx
                        qy = y + ddy
                        s = 2 if t % 2 == 1 else 0
                        c = t + Rn[s][qx][qy]
                        if c > ans:
                            ans = c
            # starts with 1 (k=1 chains) need candidate too
            for x in range(1, n + 1):
                gx = g[x]
                for y in range(1, m + 1):
                    if gx[y] == 1:
                        if ans < 1:
                            ans = 1
                        qx = x + ddx
                        qy = y + ddy
                        c = 1 + Rn[2][qx][qy]
                        if c > ans:
                            ans = c
        return ans
