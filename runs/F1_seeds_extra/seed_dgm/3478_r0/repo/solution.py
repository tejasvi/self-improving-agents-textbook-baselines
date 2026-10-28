from typing import List


class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        X, Y = xCorner, yCorner
        n = len(circles)
        parent = list(range(n + 2))  # n: arc touching bottom/right edges, n+1: arc touching left/top edges

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        def seg_d2(cx, cy, px, py):
            return (cx - px) ** 2 + (cy - py) ** 2

        BR, TL = n, n + 1
        for i, (x, y, r) in enumerate(circles):
            r2 = r * r
            # circle covers origin or corner -> blocked
            if x * x + y * y <= r2 or (x - X) ** 2 + (y - Y) ** 2 <= r2:
                return False
            # bottom edge: y=0, x in [0, X]
            cxb = min(max(x, 0), X)
            # right edge: x=X, y in [0, Y]
            cyr = min(max(y, 0), Y)
            # left edge: x=0, y in [0, Y]
            cyl = cyr
            # top edge: y=Y, x in [0, X]
            cxt = cxb
            if seg_d2(x, y, cxb, 0) <= r2 or seg_d2(x, y, X, cyr) <= r2:
                union(i, BR)
            if seg_d2(x, y, 0, cyl) <= r2 or seg_d2(x, y, cxt, Y) <= r2:
                union(i, TL)
            if find(BR) == find(TL):
                return False

        for i in range(n):
            xi, yi, ri = circles[i]
            for j in range(i + 1, n):
                xj, yj, rj = circles[j]
                if (xi - xj) ** 2 + (yi - yj) ** 2 <= (ri + rj) ** 2:
                    union(i, j)
                    
        return find(BR) != find(TL)
