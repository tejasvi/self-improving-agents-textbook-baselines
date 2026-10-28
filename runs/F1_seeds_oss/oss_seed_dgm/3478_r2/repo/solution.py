from typing import List

class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x: int, y: int):
        rx = self.find(x)
        ry = self.find(y)
        if rx == ry:
            return
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1


class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        n = len(circles)
        # indices for walls
        LEFT = n
        RIGHT = n + 1
        BOTTOM = n + 2
        TOP = n + 3
        uf = UnionFind(n + 4)
        # Union circles that intersect or touch
        for i in range(n):
            xi, yi, ri = circles[i]
            # Check contact with walls
            if xi - ri <= 0:
                uf.union(i, LEFT)
            if xi + ri >= xCorner:
                uf.union(i, RIGHT)
            if yi - ri <= 0:
                uf.union(i, BOTTOM)
            if yi + ri >= yCorner:
                uf.union(i, TOP)
            # compare with later circles to avoid double work
            for j in range(i + 1, n):
                xj, yj, rj = circles[j]
                dx = xi - xj
                dy = yi - yj
                # Use squared distance to avoid sqrt
                if dx * dx + dy * dy <= (ri + rj) * (ri + rj):
                    uf.union(i, j)
        # If any blocking connections exist, path is impossible
        if uf.find(LEFT) == uf.find(RIGHT):
            return False
        if uf.find(TOP) == uf.find(BOTTOM):
            return False
        if uf.find(LEFT) == uf.find(BOTTOM):
            return False
        if uf.find(RIGHT) == uf.find(TOP):
            return False
        return True
