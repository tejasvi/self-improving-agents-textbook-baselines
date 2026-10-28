from typing import List
import math

class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> None:
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

        # Union circles with walls and check corners
        for i in range(n):
            xi, yi, ri = circles[i]
            # Touching walls
            if xi - ri <= 0:
                uf.union(i, LEFT)
            if xi + ri >= xCorner:
                uf.union(i, RIGHT)
            if yi - ri <= 0:
                uf.union(i, BOTTOM)
            if yi + ri >= yCorner:
                uf.union(i, TOP)
            # Corner inside or touching a circle blocks immediately
            if xi * xi + yi * yi <= ri * ri:
                return False
            if (xi - xCorner) ** 2 + (yi - yCorner) ** 2 <= ri * ri:
                return False

        # Union overlapping/touching circles
        for i in range(n):
            xi, yi, ri = circles[i]
            for j in range(i + 1, n):
                xj, yj, rj = circles[j]
                dx = xi - xj
                dy = yi - yj
                if dx * dx + dy * dy <= (ri + rj) * (ri + rj):
                    uf.union(i, j)

        # Check blocking configurations
        left_root = uf.find(LEFT)
        right_root = uf.find(RIGHT)
        top_root = uf.find(TOP)
        bottom_root = uf.find(BOTTOM)

        # Any connection that blocks the path?
        if left_root == right_root:
            return False  # left wall connected to right wall
        if top_root == bottom_root:
            return False  # top wall connected to bottom wall
        if left_root == bottom_root:
            return False  # start corner enclosed
        if right_root == top_root:
            return False  # end corner enclosed
        # Note: connections like left-top or bottom-right do not block the path
        return True
