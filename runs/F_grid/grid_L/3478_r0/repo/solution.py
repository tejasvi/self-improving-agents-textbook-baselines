from typing import List


class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        X, Y = xCorner, yCorner
        n = len(circles)
        # nodes 0..n-1: circles; n: top-left wall; n+1: bottom-right wall
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

        def sq_dist_to_segment(px, py, ax, ay, bx, by):
            # squared distance from point to axis-aligned segment (exact)
            cx = min(max(px, min(ax, bx)), max(ax, bx))
            cy = min(max(py, min(ay, by)), max(ay, by))
            return (px - cx) ** 2 + (py - cy) ** 2

        TL, BR = n, n + 1
        for i, (x, y, r) in enumerate(circles):
            r2 = r * r
            # circle covers a corner -> blocked
            if x * x + y * y <= r2 or (x - X) ** 2 + (y - Y) ** 2 <= r2:
                return False
            # touches top-left wall: left edge (0,0)-(0,Y) or top edge (0,Y)-(X,Y)
            if (sq_dist_to_segment(x, y, 0, 0, 0, Y) <= r2 or
                    sq_dist_to_segment(x, y, 0, Y, X, Y) <= r2):
                union(i, TL)
            # touches bottom-right wall: bottom edge (0,0)-(X,0) or right edge (X,0)-(X,Y)
            if (sq_dist_to_segment(x, y, 0, 0, X, 0) <= r2 or
                    sq_dist_to_segment(x, y, X, 0, X, Y) <= r2):
                union(i, BR)

        for i in range(n):
            xi, yi, ri = circles[i]
            for j in range(i + 1, n):
                xj, yj, rj = circles[j]
                if (xi - xj) ** 2 + (yi - yj) ** 2 <= (ri + rj) ** 2:
                    union(i, j)

        return find(TL) != find(BR)
