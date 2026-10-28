from typing import List


class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        X, Y = xCorner, yCorner
        n = len(circles)
        # nodes 0..n-1: circles; n: arc A (left+top edges); n+1: arc B (bottom+right edges)
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

        def seg_dist2(px, py, ax, ay, bx, by):
            # squared distance from point to segment [a,b] (axis-aligned)
            cx = min(max(px, min(ax, bx)), max(ax, bx))
            cy = min(max(py, min(ay, by)), max(ay, by))
            return (px - cx) ** 2 + (py - cy) ** 2

        A = n
        B = n + 1
        for i, (x, y, r) in enumerate(circles):
            r2 = r * r
            # circle covers a corner -> impossible
            if x * x + y * y <= r2 or (x - X) ** 2 + (y - Y) ** 2 <= r2:
                return False
            # touches left edge (0,0)-(0,Y) or top edge (0,Y)-(X,Y) -> arc A
            if seg_dist2(x, y, 0, 0, 0, Y) <= r2 or seg_dist2(x, y, 0, Y, X, Y) <= r2:
                union(i, A)
            # touches bottom edge (0,0)-(X,0) or right edge (X,0)-(X,Y) -> arc B
            if seg_dist2(x, y, 0, 0, X, 0) <= r2 or seg_dist2(x, y, X, 0, X, Y) <= r2:
                union(i, B)
            for j in range(i):
                x2, y2, r3 = circles[j]
                if (x - x2) ** 2 + (y - y2) ** 2 <= (r + r3) ** 2:
                    union(i, j)
            if find(A) == find(B):
                return False
        return find(A) != find(B)
