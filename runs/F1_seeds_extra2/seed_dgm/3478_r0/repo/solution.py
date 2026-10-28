from typing import List


class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        n = len(circles)
        # nodes 0..n-1: circles; n: wall A (top-left edges); n+1: wall B (bottom-right edges)
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

        def sq_dist_to_seg(px, py, x1, y1, x2, y2):
            # axis-aligned segment from (x1,y1) to (x2,y2)
            cx = min(max(px, min(x1, x2)), max(x1, x2))
            cy = min(max(py, min(y1, y2)), max(y1, y2))
            return (px - cx) ** 2 + (py - cy) ** 2

        A = n
        B = n + 1
        for i, (x, y, r) in enumerate(circles):
            # circle covering a corner blocks the path entirely
            if x * x + y * y <= r * r:
                return False
            if (x - xCorner) ** 2 + (y - yCorner) ** 2 <= r * r:
                return False
            r2 = r * r
            # touches top-left boundary: left edge x=0, y in [0,yC]; top edge y=yC, x in [0,xC]
            if sq_dist_to_seg(x, y, 0, 0, 0, yCorner) <= r2 or \
               sq_dist_to_seg(x, y, 0, yCorner, xCorner, yCorner) <= r2:
                union(i, A)
            # touches bottom-right boundary: bottom edge y=0, x in [0,xC]; right edge x=xC, y in [0,yC]
            if sq_dist_to_seg(x, y, 0, 0, xCorner, 0) <= r2 or \
               sq_dist_to_seg(x, y, xCorner, 0, xCorner, yCorner) <= r2:
                union(i, B)

        for i in range(n):
            xi, yi, ri = circles[i]
            for j in range(i + 1, n):
                xj, yj, rj = circles[j]
                if (xi - xj) ** 2 + (yi - yj) ** 2 <= (ri + rj) ** 2:
                    union(i, j)

        return find(A) != find(B)
