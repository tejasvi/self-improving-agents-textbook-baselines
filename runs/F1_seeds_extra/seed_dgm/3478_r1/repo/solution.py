from typing import List


class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        X, Y = xCorner, yCorner
        n = len(circles)
        # nodes: 0..n-1 circles, n = wall A (left + top edges), n+1 = wall B (bottom + right edges)
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

        WA, WB = n, n + 1
        for i, (cx, cy, r) in enumerate(circles):
            r2 = r * r
            # left edge: x=0, y in [0, Y]
            cyl = min(max(cy, 0), Y)
            if cx * cx + (cy - cyl) ** 2 <= r2:
                union(i, WA)
            # top edge: y=Y, x in [0, X]
            cxt = min(max(cx, 0), X)
            if (cx - cxt) ** 2 + (cy - Y) ** 2 <= r2:
                union(i, WA)
            # bottom edge: y=0, x in [0, X]
            if (cx - cxt) ** 2 + cy * cy <= r2:
                union(i, WB)
            # right edge: x=X, y in [0, Y]
            if (cx - X) ** 2 + (cy - cyl) ** 2 <= r2:
                union(i, WB)

        for i in range(n):
            xi, yi, ri = circles[i]
            for j in range(i + 1, n):
                xj, yj, rj = circles[j]
                if (xi - xj) ** 2 + (yi - yj) ** 2 <= (ri + rj) ** 2:
                    union(i, j)

        return find(WA) != find(WB)
