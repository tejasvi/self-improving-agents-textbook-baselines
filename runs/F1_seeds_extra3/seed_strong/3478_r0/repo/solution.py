from typing import *


class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        n = len(circles)
        parent = list(range(n + 2))
        A = n      # left edge + top edge
        B = n + 1  # bottom edge + right edge

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        def seg_touch(cx, cy, r, x1, y1, x2, y2):
            # squared distance from center to axis-aligned segment <= r^2
            px = min(max(cx, x1), x2)
            py = min(max(cy, y1), y2)
            return (px - cx) ** 2 + (py - cy) ** 2 <= r * r

        for i, (x, y, r) in enumerate(circles):
            # left edge: (0,0)-(0,yC); top edge: (0,yC)-(xC,yC)
            if seg_touch(x, y, r, 0, 0, 0, yCorner) or seg_touch(x, y, r, 0, yCorner, xCorner, yCorner):
                union(i, A)
            # bottom edge: (0,0)-(xC,0); right edge: (xC,0)-(xC,yC)
            if seg_touch(x, y, r, 0, 0, xCorner, 0) or seg_touch(x, y, r, xCorner, 0, xCorner, yCorner):
                union(i, B)
            for j in range(i):
                x2, y2, r2 = circles[j]
                if (x - x2) ** 2 + (y - y2) ** 2 <= (r + r2) ** 2:
                    union(i, j)

        return find(A) != find(B)
