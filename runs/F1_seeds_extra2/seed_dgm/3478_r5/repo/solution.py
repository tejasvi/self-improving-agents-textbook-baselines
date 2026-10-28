from typing import List


class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        X, Y = xCorner, yCorner

        def seg_d2(px, py, ax, ay, bx, by):
            # squared distance from point to axis-aligned segment [a,b]
            cx = min(max(px, min(ax, bx)), max(ax, bx))
            cy = min(max(py, min(ay, by)), max(ay, by))
            return (px - cx) ** 2 + (py - cy) ** 2

        n = len(circles)
        # nodes 0..n-1 circles, n = top-left arc, n+1 = bottom-right arc
        parent = list(range(n + 2))

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        TL, BR = n, n + 1
        for i, (x, y, r) in enumerate(circles):
            r2 = r * r
            # origin or far corner covered by a circle => unreachable
            if x * x + y * y <= r2 or (x - X) ** 2 + (y - Y) ** 2 <= r2:
                return False
            # top-left arc: left edge (0,0)-(0,Y) and top edge (0,Y)-(X,Y)
            if (seg_d2(x, y, 0, 0, 0, Y) <= r2 or
                    seg_d2(x, y, 0, Y, X, Y) <= r2):
                union(i, TL)
            # bottom-right arc: bottom edge (0,0)-(X,0) and right edge (X,0)-(X,Y)
            if (seg_d2(x, y, 0, 0, X, 0) <= r2 or
                    seg_d2(x, y, X, 0, X, Y) <= r2):
                union(i, BR)

        for i in range(n):
            xi, yi, ri = circles[i]
            for j in range(i + 1, n):
                xj, yj, rj = circles[j]
                if (xi - xj) ** 2 + (yi - yj) ** 2 <= (ri + rj) ** 2:
                    union(i, j)

        return find(TL) != find(BR)
