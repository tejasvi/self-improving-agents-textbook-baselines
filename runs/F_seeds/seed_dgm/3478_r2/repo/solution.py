from typing import List


class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        X, Y = xCorner, yCorner
        n = len(circles)
        A, C = n, n + 1
        parent = list(range(n + 2))

        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u

        def union(u, v):
            ru, rv = find(u), find(v)
            if ru != rv:
                parent[ru] = rv

        def dist2_to_segment(px, py, ax, ay, bx, by):
            # squared distance from point to axis-aligned segment [a,b]
            cx = min(max(px, min(ax, bx)), max(ax, bx))
            cy = min(max(py, min(ay, by)), max(ay, by))
            return (px - cx) ** 2 + (py - cy) ** 2

        for i, (x, y, r) in enumerate(circles):
            r2 = r * r
            # bottom edge: (0,0)-(X,0); right edge: (X,0)-(X,Y)
            if dist2_to_segment(x, y, 0, 0, X, 0) <= r2 or \
               dist2_to_segment(x, y, X, 0, X, Y) <= r2:
                union(i, A)
            # left edge: (0,0)-(0,Y); top edge: (0,Y)-(X,Y)
            if dist2_to_segment(x, y, 0, 0, 0, Y) <= r2 or \
               dist2_to_segment(x, y, 0, Y, X, Y) <= r2:
                union(i, C)
            for j in range(i):
                x2, y2, r2b = circles[j]
                rs = r + r2b
                if (x - x2) ** 2 + (y - y2) ** 2 <= rs * rs:
                    union(i, j)

        return find(A) != find(C)
