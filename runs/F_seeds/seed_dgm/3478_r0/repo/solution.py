from typing import List


class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        X, Y = xCorner, yCorner
        n = len(circles)
        # Nodes: 0 = left wall (x=0), 1 = top wall (y=Y),
        #        2 = right wall (x=X), 3 = bottom wall (y=0), 4+i = circle i
        parent = list(range(n + 4))

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        def clamp(v, lo, hi):
            return lo if v < lo else hi if v > hi else v

        for i, (x, y, r) in enumerate(circles):
            node = 4 + i
            # Circle covers origin or the far corner -> impossible
            if x * x + y * y <= r * r:
                return False
            if (X - x) ** 2 + (Y - y) ** 2 <= r * r:
                return False
            # Left wall: segment x=0, y in [0, Y]
            py = clamp(y, 0, Y)
            if x * x + (y - py) ** 2 <= r * r:
                union(node, 0)
            # Top wall: segment y=Y, x in [0, X]
            px = clamp(x, 0, X)
            if (x - px) ** 2 + (Y - y) ** 2 <= r * r:
                union(node, 1)
            # Right wall: segment x=X, y in [0, Y]
            if (X - x) ** 2 + (y - py) ** 2 <= r * r:
                union(node, 2)
            # Bottom wall: segment y=0, x in [0, X]
            if (x - px) ** 2 + y * y <= r * r:
                union(node, 3)

        # Circles overlapping (touching counts as blocking)
        for i in range(n):
            x1, y1, r1 = circles[i]
            for j in range(i + 1, n):
                x2, y2, r2 = circles[j]
                if (x1 - x2) ** 2 + (y1 - y2) ** 2 <= (r1 + r2) ** 2:
                    union(4 + i, 4 + j)

        # Blocked if left or top wall joins bottom or right wall
        for a in (0, 1):
            for b in (2, 3):
                if find(a) == find(b):
                    return False
        return True
