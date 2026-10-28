from typing import *


class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        n = len(points)
        u = [x + y for x, y in points]
        v = [x - y for x, y in points]
        # Only removing an extremum of u or v can reduce the diameter.
        candidates = {
            u.index(max(u)), u.index(min(u)),
            v.index(max(v)), v.index(min(v)),
        }
        best = None
        for c in candidates:
            mu_max = mu_min = None
            mv_max = mv_min = None
            for i in range(n):
                if i == c:
                    continue
                a = u[i]
                b = v[i]
                if mu_max is None:
                    mu_max = mu_min = a
                    mv_max = mv_min = b
                else:
                    if a > mu_max: mu_max = a
                    if a < mu_min: mu_min = a
                    if b > mv_max: mv_max = b
                    if b < mv_min: mv_min = b
            d = max(mu_max - mu_min, mv_max - mv_min)
            if best is None or d < best:
                best = d
        return best
