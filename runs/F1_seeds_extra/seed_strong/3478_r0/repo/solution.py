from typing import *


class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        X, Y = xCorner, yCorner
        n = len(circles)
        parent = list(range(n + 2))
        TL, BR = n, n + 1

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        def seg_d2(px, py, ax, ay, bx, by):
            # squared distance from point to axis-aligned segment
            dx = 0 if ax <= px <= bx or bx <= px <= ax else min(abs(px - ax), abs(px - bx))
            dy = 0 if ay <= py <= by or by <= py <= ay else min(abs(py - ay), abs(py - by))
            return dx * dx + dy * dy

        for i, (x, y, r) in enumerate(circles):
            r2 = r * r
            if x * x + y * y <= r2 or (x - X) ** 2 + (y - Y) ** 2 <= r2:
                return False
            # top-left boundary: left edge and top edge
            if (seg_d2(x, y, 0, 0, 0, Y) <= r2 or seg_d2(x, y, 0, Y, X, Y) <= r2):
                union(i, TL)
            # bottom-right boundary: bottom edge and right edge
            if (seg_d2(x, y, 0, 0, X, 0) <= r2 or seg_d2(x, y, X, 0, X, Y) <= r2):
                union(i, BR)

        for i in range(n):
            x1, y1, r1 = circles[i]
            for j in range(i + 1, n):
                x2, y2, r2 = circles[j]
                s = r1 + r2
                if (x1 - x2) ** 2 + (y1 - y2) ** 2 <= s * s:
                    union(i, j)

        return find(TL) != find(BR)
