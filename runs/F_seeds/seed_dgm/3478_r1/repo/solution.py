from typing import List


class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        n = len(circles)
        # Nodes 0..n-1: circles; n: arc A (left + top edges); n+1: arc B (bottom + right edges)
        parent = list(range(n + 2))

        def find(a: int) -> int:
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        A, B = n, n + 1

        # Corners must not be covered by any circle.
        for x, y, r in circles:
            r2 = r * r
            if x * x + y * y <= r2:
                return False
            if (x - xCorner) ** 2 + (y - yCorner) ** 2 <= r2:
                return False

        for i, (x, y, r) in enumerate(circles):
            r2 = r * r
            # Distance squared to left edge {0} x [0, yCorner]
            cy = min(max(y, 0), yCorner)
            if x * x + (y - cy) ** 2 <= r2:
                union(i, A)
            # Distance squared to top edge [0, xCorner] x {yCorner}
            cx = min(max(x, 0), xCorner)
            if (x - cx) ** 2 + (y - yCorner) ** 2 <= r2:
                union(i, A)
            # Distance squared to bottom edge [0, xCorner] x {0}
            if (x - cx) ** 2 + y * y <= r2:
                union(i, B)
            # Distance squared to right edge {xCorner} x [0, yCorner]
            if (x - xCorner) ** 2 + (y - cy) ** 2 <= r2:
                union(i, B)

        # Circles touching each other
        for i in range(n):
            xi, yi, ri = circles[i]
            for j in range(i + 1, n):
                xj, yj, rj = circles[j]
                if (xi - xj) ** 2 + (yi - yj) ** 2 <= (ri + rj) ** 2:
                    union(i, j)

        return find(A) != find(B)
