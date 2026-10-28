from typing import List


class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        n = len(circles)
        # Nodes: circles 0..n-1, then walls.
        B, R, L, T = n, n + 1, n + 2, n + 3
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

        def seg_dist_sq(px, py, ax, ay, bx, by):
            # squared distance from point to axis-aligned segment
            cx = min(max(px, min(ax, bx)), max(ax, bx))
            cy = min(max(py, min(ay, by)), max(ay, by))
            return (px - cx) ** 2 + (py - cy) ** 2

        X, Y = xCorner, yCorner
        for i, (x, y, r) in enumerate(circles):
            r2 = r * r
            # Circle covering either corner blocks immediately.
            if x * x + y * y <= r2 or (x - X) ** 2 + (y - Y) ** 2 <= r2:
                return False
            # Touching walls (within the rectangle's sides).
            if seg_dist_sq(x, y, 0, 0, X, 0) <= r2:
                union(i, B)
            if seg_dist_sq(x, y, 0, Y, X, Y) <= r2:
                union(i, T)
            if seg_dist_sq(x, y, 0, 0, 0, Y) <= r2:
                union(i, L)
            if seg_dist_sq(x, y, X, 0, X, Y) <= r2:
                union(i, R)
            # Circle-circle overlap or touching.
            for j in range(i):
                x2, y2, r3 = circles[j]
                if (x - x2) ** 2 + (y - y2) ** 2 <= (r + r3) ** 2:
                    union(i, j)

        for a, b in ((B, L), (B, T), (R, L), (R, T)):
            if find(a) == find(b):
                return False
        return True
