from typing import List


class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        X, Y = xCorner, yCorner
        n = len(circles)
        parent = list(range(n + 2))
        BR = n      # bottom / right edges
        TL = n + 1  # top / left edges

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        def seg_hit(c, d2, lo, hi):
            # interval [c-d, c+d] (d^2 = d2) intersects [0, hi]; c >= 0 assumed
            return c <= hi or (c - hi) * (c - hi) <= d2

        for i, (x, y, r) in enumerate(circles):
            r2 = r * r
            # circle contains a corner -> blocked
            if x * x + y * y <= r2 or (x - X) ** 2 + (y - Y) ** 2 <= r2:
                return False
            # bottom edge y=0, x in [0,X]
            if y <= r and seg_hit(x, r2 - y * y, 0, X):
                union(i, BR)
            # right edge x=X, y in [0,Y]
            if abs(x - X) <= r and seg_hit(y, r2 - (x - X) ** 2, 0, Y):
                union(i, BR)
            # top edge y=Y, x in [0,X]
            if abs(y - Y) <= r and seg_hit(x, r2 - (y - Y) ** 2, 0, X):
                union(i, TL)
            # left edge x=0, y in [0,Y]
            if x <= r and seg_hit(y, r2 - x * x, 0, Y):
                union(i, TL)

        for i in range(n):
            for j in range(i + 1, n):
                dx = circles[i][0] - circles[j][0]
                dy = circles[i][1] - circles[j][1]
                rs = circles[i][2] + circles[j][2]
                if dx * dx + dy * dy <= rs * rs:
                    union(i, j)

        return find(BR) != find(TL)
