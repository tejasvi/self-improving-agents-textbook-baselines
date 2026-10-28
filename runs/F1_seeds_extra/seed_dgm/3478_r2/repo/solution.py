from typing import List


class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        X, Y = xCorner, yCorner

        def seg_touch(px, py, ax, ay, bx, by, r2):
            # exact test: squared distance from point to segment AB <= r2
            dx, dy = bx - ax, by - ay
            L2 = dx * dx + dy * dy
            t = (px - ax) * dx + (py - ay) * dy
            if t <= 0:
                return (px - ax) ** 2 + (py - ay) ** 2 <= r2
            if t >= L2:
                return (px - bx) ** 2 + (py - by) ** 2 <= r2
            cross = (px - ax) * dy - (py - ay) * dx
            return cross * cross <= r2 * L2

        n = len(circles)
        LT = n      # boundary arc (0,0)->(0,Y)->(X,Y)
        RB = n + 1  # boundary arc (0,0)->(X,0)->(X,Y)
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

        for i, (x, y, r) in enumerate(circles):
            r2 = r * r
            if x * x + y * y <= r2 or (x - X) ** 2 + (y - Y) ** 2 <= r2:
                return False
            if (seg_touch(x, y, 0, 0, 0, Y, r2) or seg_touch(x, y, 0, Y, X, Y, r2)):
                union(i, LT)
            if (seg_touch(x, y, 0, 0, X, 0, r2) or seg_touch(x, y, X, 0, X, Y, r2)):
                union(i, RB)
            for j in range(i):
                x2, y2, r3 = circles[j]
                s = r + r3
                if (x - x2) ** 2 + (y - y2) ** 2 <= s * s:
                    union(i, j)

        return find(LT) != find(RB)
