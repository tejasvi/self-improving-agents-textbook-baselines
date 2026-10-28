from typing import List

class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        # Union-Find (Disjoint Set Union) implementation
        n = len(circles)
        parent = list(range(n + 4))  # extra 4 for walls: left, right, bottom, top
        rank = [0] * (n + 4)

        LEFT, RIGHT, BOTTOM, TOP = n, n + 1, n + 2, n + 3

        def find(u: int) -> int:
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u

        def union(u: int, v: int) -> None:
            ru, rv = find(u), find(v)
            if ru == rv:
                return
            if rank[ru] < rank[rv]:
                parent[ru] = rv
            elif rank[ru] > rank[rv]:
                parent[rv] = ru
            else:
                parent[rv] = ru
                rank[ru] += 1

        # Helper to check if two circles intersect or touch
        def circles_touch(i: int, j: int) -> bool:
            x1, y1, r1 = circles[i]
            x2, y2, r2 = circles[j]
            dx = x1 - x2
            dy = y1 - y2
            dist_sq = dx * dx + dy * dy
            rad_sum = r1 + r2
            return dist_sq <= rad_sum * rad_sum

        # Process each circle: union with walls if touching, and check start/end inside
        for i, (x, y, r) in enumerate(circles):
            # If start or end lies inside a circle -> impossible
            if x * x + y * y <= r * r:
                return False  # contains (0,0)
            dx_end = x - xCorner
            dy_end = y - yCorner
            if dx_end * dx_end + dy_end * dy_end <= r * r:
                return False  # contains (xCorner, yCorner)

            # Touch walls?
            if x - r <= 0:
                union(i, LEFT)
            if x + r >= xCorner:
                union(i, RIGHT)
            if y - r <= 0:
                union(i, BOTTOM)
            if y + r >= yCorner:
                union(i, TOP)

        # Union intersecting circles
        for i in range(n):
            for j in range(i + 1, n):
                if circles_touch(i, j):
                    union(i, j)

        # If any blocking connection exists, return False
        if find(LEFT) == find(RIGHT):
            return False
        if find(TOP) == find(BOTTOM):
            return False
        if find(LEFT) == find(BOTTOM):
            return False
        if find(RIGHT) == find(TOP):
            return False

        return True
