from typing import *


class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        X, Y = xCorner, yCorner

        def seg_d2(px, py, ax, ay, bx, by):
            # squared distance from point to axis-aligned segment [a,b]
            cx = min(max(px, min(ax, bx)), max(ax, bx))
            cy = min(max(py, min(ay, by)), max(ay, by))
            return (px - cx) ** 2 + (py - cy) ** 2

        # Blocking analysis: the path is blocked iff a chain of obstacles
        # (circles touching/overlapping, where touching counts) connects the
        # arc A = left+top edges to arc B = bottom+right edges, or a circle
        # covers a corner. Circles not meeting the boundary are irrelevant.
        cs = []
        for x, y, r in circles:
            r2 = r * r
            if x * x + y * y <= r2 or (x - X) ** 2 + (y - Y) ** 2 <= r2:
                return False  # covers a corner
            if min(seg_d2(x, y, 0, 0, X, 0), seg_d2(x, y, 0, Y, X, Y),
                   seg_d2(x, y, 0, 0, 0, Y), seg_d2(x, y, X, 0, X, Y)) <= r2:
                cs.append((x, y, r))

        n = len(cs)
        # nodes 0..n-1 circles, n = arc A (left/top), n+1 = arc B (bottom/right)
        parent = list(range(n + 2))

        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        A, B = n, n + 1
        for i, (x, y, r) in enumerate(cs):
            r2 = r * r
            if seg_d2(x, y, 0, 0, 0, Y) <= r2 or seg_d2(x, y, 0, Y, X, Y) <= r2:
                union(i, A)
            if seg_d2(x, y, 0, 0, X, 0) <= r2 or seg_d2(x, y, X, 0, X, Y) <= r2:
                union(i, B)
        for i in range(n):
            xi, yi, ri = cs[i]
            for j in range(i + 1, n):
                xj, yj, rj = cs[j]
                if (xi - xj) ** 2 + (yi - yj) ** 2 <= (ri + rj) ** 2:
                    union(i, j)
        return find(A) != find(B)
