from typing import List


class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        n = len(circles)
        # nodes 0..n-1 are circles, n = wall touching top/left arc, n+1 = wall touching bottom/right arc
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

        A, B = n, n + 1

        def clamp(v, lo, hi):
            return lo if v < lo else (hi if v > hi else v)

        for i, (x, y, r) in enumerate(circles):
            r2 = r * r
            # circle covers origin or far corner -> blocked
            if x * x + y * y <= r2:
                return False
            if (x - xCorner) ** 2 + (y - yCorner) ** 2 <= r2:
                return False

            # left edge x=0, y in [0, yCorner]
            py = clamp(y, 0, yCorner)
            if x * x + (y - py) ** 2 <= r2:
                union(i, A)
            # top edge y=yCorner, x in [0, xCorner]
            px = clamp(x, 0, xCorner)
            if (x - px) ** 2 + (y - yCorner) ** 2 <= r2:
                union(i, A)
            # bottom edge y=0, x in [0, xCorner]
            if (x - px) ** 2 + y * y <= r2:
                union(i, B)
            # right edge x=xCorner, y in [0, yCorner]
            if (x - xCorner) ** 2 + (y - py) ** 2 <= r2:
                union(i, B)

        for i in range(n):
            for j in range(i + 1, n):
                x1, y1, r1 = circles[i]
                x2, y2, r2_ = circles[j]
                if (x1 - x2) ** 2 + (y1 - y2) ** 2 <= (r1 + r2_) ** 2:
                    union(i, j)

        return find(A) != find(B)
