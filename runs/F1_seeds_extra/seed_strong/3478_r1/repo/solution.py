from typing import *


class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        n = len(circles)
        # DSU nodes: 0..n-1 circles, n = left, n+1 = top, n+2 = bottom, n+3 = right
        parent = list(range(n + 4))

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        L, T, B, R = n, n + 1, n + 2, n + 3
        X, Y = xCorner, yCorner

        for i, (x, y, r) in enumerate(circles):
            r2 = r * r
            # distance^2 to left segment x=0, y in [0,Y]
            dy = 0 if 0 <= y <= Y else (y if y < 0 else y - Y)
            if x * x + dy * dy <= r2:
                union(i, L)
            # top segment y=Y, x in [0,X]
            dx = 0 if 0 <= x <= X else (x if x < 0 else x - X)
            if dx * dx + (Y - y) ** 2 <= r2:
                union(i, T)
            # bottom segment y=0, x in [0,X]
            if dx * dx + y * y <= r2:
                union(i, B)
            # right segment x=X, y in [0,Y]
            dy2 = 0 if 0 <= y <= Y else (y if y < 0 else y - Y)
            if (X - x) ** 2 + dy2 * dy2 <= r2:
                union(i, R)

        for i in range(n):
            x1, y1, r1 = circles[i]
            for j in range(i + 1, n):
                x2, y2, r2_ = circles[j]
                s = r1 + r2_
                if (x1 - x2) ** 2 + (y1 - y2) ** 2 <= s * s:
                    union(i, j)

        fl, ft, fb, fr = find(L), find(T), find(B), find(R)
        if fl == fb or fl == fr or ft == fb or ft == fr:
            return False
        return True
