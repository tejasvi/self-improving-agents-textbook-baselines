from typing import List

class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        n = len(circles)
        # Union-Find structure
        parent = list(range(n + 4))  # extra 4 for left, right, bottom, top
        rank = [0] * (n + 4)

        LEFT, RIGHT, BOTTOM, TOP = n, n + 1, n + 2, n + 3

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int):
            ra, rb = find(a), find(b)
            if ra == rb:
                return
            if rank[ra] < rank[rb]:
                parent[ra] = rb
            elif rank[ra] > rank[rb]:
                parent[rb] = ra
            else:
                parent[rb] = ra
                rank[ra] += 1

        # Connect circles that intersect or touch
        for i in range(n):
            xi, yi, ri = circles[i]
            # Touch rectangle sides?
            if xi - ri <= 0:
                union(i, LEFT)
            if xi + ri >= xCorner:
                union(i, RIGHT)
            if yi - ri <= 0:
                union(i, BOTTOM)
            if yi + ri >= yCorner:
                union(i, TOP)
            for j in range(i + 1, n):
                xj, yj, rj = circles[j]
                dx = xi - xj
                dy = yi - yj
                # Use squared distances to avoid float
                if dx * dx + dy * dy <= (ri + rj) * (ri + rj):
                    union(i, j)

        # If any blocking connection exists, path is impossible
        if find(LEFT) == find(RIGHT):
            return False
        if find(TOP) == find(BOTTOM):
            return False
        if find(LEFT) == find(BOTTOM):
            return False
        if find(TOP) == find(RIGHT):
            return False
        return True
