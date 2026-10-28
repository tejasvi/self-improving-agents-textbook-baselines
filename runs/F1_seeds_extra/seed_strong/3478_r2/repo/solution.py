from typing import *


class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        X, Y = xCorner, yCorner
        n = len(circles)
        # nodes: 0..n-1 circles; n=left, n+1=top, n+2=bottom, n+3=right
        L, T, B, R = n, n + 1, n + 2, n + 3
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

        for x, y, r in circles:
            r2 = r * r
            # origin or far corner covered by a circle
            if x * x + y * y <= r2 or (X - x) ** 2 + (Y - y) ** 2 <= r2:
                return False

        def dist2_to_segment_x(x, y, wx):
            # distance^2 from (x,y) to segment {wx} x [0,Y]
            dy = 0
            if y < 0:
                dy = -y
            elif y > Y:
                dy = y - Y
            return (x - wx) ** 2 + dy * dy

        def dist2_to_segment_y(x, y, wy):
            # distance^2 from (x,y) to segment [0,X] x {wy}
            dx = 0
            if x < 0:
                dx = -x
            elif x > X:
                dx = x - X
            return (y - wy) ** 2 + dx * dx

        for i, (x, y, r) in enumerate(circles):
            r2 = r * r
            if dist2_to_segment_x(x, y, 0) <= r2:
                union(i, L)
            if dist2_to_segment_x(x, y, X) <= r2:
                union(i, R)
            if dist2_to_segment_y(x, y, 0) <= r2:
                union(i, B)
            if dist2_to_segment_y(x, y, Y) <= r2:
                union(i, T)
            for j in range(i):
                xj, yj, rj = circles[j]
                s = r + rj
                if (x - xj) ** 2 + (y - yj) ** 2 <= s * s:
                    union(i, j)

        for a, b in ((L, B), (L, R), (T, B), (T, R)):
            if find(a) == find(b):
                return False
        return True
