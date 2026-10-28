from typing import *


class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        n = len(circles)
        # nodes 0..n-1 circles; n = arc A (bottom/right walls); n+1 = arc B (top/left walls)
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
        for i, (x, y, r) in enumerate(circles):
            r2 = r * r
            # left wall x=0, y in [0, yCorner]
            cy = min(max(y, 0), yCorner)
            if x * x + (y - cy) ** 2 <= r2:
                union(i, B)
            # top wall y=yCorner, x in [0, xCorner]
            cx = min(max(x, 0), xCorner)
            if (x - cx) ** 2 + (y - yCorner) ** 2 <= r2:
                union(i, B)
            # bottom wall y=0, x in [0, xCorner]
            if (x - cx) ** 2 + y * y <= r2:
                union(i, A)
            # right wall x=xCorner, y in [0, yCorner]
            if (x - xCorner) ** 2 + (y - cy) ** 2 <= r2:
                union(i, A)

        if find(A) == find(B):
            return False

        for i in range(n):
            xi, yi, ri = circles[i]
            for j in range(i + 1, n):
                xj, yj, rj = circles[j]
                if (xi - xj) ** 2 + (yi - yj) ** 2 <= (ri + rj) ** 2:
                    union(i, j)
                    if find(A) == find(B):
                        return False
        return find(A) != find(B)
