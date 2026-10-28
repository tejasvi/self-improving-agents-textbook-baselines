from typing import *


class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        X, Y = xCorner, yCorner
        n = len(circles)
        parent = list(range(n + 2))  # n: top-left wall, n+1: bottom-right wall

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        def d2_seg_box(px, py, x1, y1, x2, y2):
            # squared distance from point to axis-aligned segment box
            cx = min(max(px, x1), x2)
            cy = min(max(py, y1), y2)
            return (px - cx) * (px - cx) + (py - cy) * (py - cy)

        TL = n
        BR = n + 1
        for i, (x, y, r) in enumerate(circles):
            r2 = r * r
            # origin or corner inside/on circle -> blocked
            if x * x + y * y <= r2 or (x - X) ** 2 + (y - Y) ** 2 <= r2:
                return False
            # touches top-left walls: left edge (x=0, y in [0,Y]) or top edge (y=Y, x in [0,X])
            if d2_seg_box(x, y, 0, 0, 0, Y) <= r2 or d2_seg_box(x, y, 0, Y, X, Y) <= r2:
                union(i, TL)
            # touches bottom-right walls: bottom edge (y=0, x in [0,X]) or right edge (x=X, y in [0,Y])
            if d2_seg_box(x, y, 0, 0, X, 0) <= r2 or d2_seg_box(x, y, X, 0, X, Y) <= r2:
                union(i, BR)

        for i in range(n):
            xi, yi, ri = circles[i]
            for j in range(i + 1, n):
                xj, yj, rj = circles[j]
                s = ri + rj
                if (xi - xj) ** 2 + (yi - yj) ** 2 <= s * s:
                    union(i, j)

        return find(TL) != find(BR)
