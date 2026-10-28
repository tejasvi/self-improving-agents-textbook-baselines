from typing import *


class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        X, Y = xCorner, yCorner
        n = len(circles)
        parent = list(range(n + 2))
        A, B = n, n + 1  # A: left+top sides, B: bottom+right sides

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        for i, (x, y, r) in enumerate(circles):
            r2 = r * r
            # a circle covering either corner blocks the path
            if x * x + y * y <= r2 or (X - x) ** 2 + (Y - y) ** 2 <= r2:
                return False
            # squared distance from center to each side segment
            dl = x * x if 0 <= y <= Y else x * x + min(y * y, (y - Y) ** 2)   # left x=0
            dt = (y - Y) ** 2 if 0 <= x <= X else (y - Y) ** 2 + min(x * x, (x - X) ** 2)  # top y=Y
            db = y * y if 0 <= x <= X else y * y + min(x * x, (x - X) ** 2)  # bottom y=0
            dr = (X - x) ** 2 if 0 <= y <= Y else (X - x) ** 2 + min(y * y, (y - Y) ** 2)  # right x=X
            if min(dl, dt) <= r2:
                union(i, A)
            if min(db, dr) <= r2:
                union(i, B)

        for i in range(n):
            x1, y1, r1 = circles[i]
            for j in range(i + 1, n):
                x2, y2, r2_ = circles[j]
                if (x1 - x2) ** 2 + (y1 - y2) ** 2 <= (r1 + r2_) ** 2:
                    union(i, j)

        return find(A) != find(B)
