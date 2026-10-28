from typing import *


class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        n = len(points)
        us = [x + y for x, y in points]
        vs = [x - y for x, y in points]
        # Removing a non-extreme point leaves the full range, which is never
        # better than removing an extreme one, so only test extreme indices.
        cands = set()
        for arr in (us, vs):
            order = sorted(range(n), key=arr.__getitem__)
            cands.update(order[:2])
            cands.update(order[-2:])
        best = None
        for r in cands:
            mu_max = mu_min = None
            mv_max = mv_min = None
            for i in range(n):
                if i == r:
                    continue
                u = us[i]
                v = vs[i]
                if mu_max is None:
                    mu_max = mu_min = u
                    mv_max = mv_min = v
                else:
                    if u > mu_max: mu_max = u
                    elif u < mu_min: mu_min = u
                    if v > mv_max: mv_max = v
                    elif v < mv_min: mv_min = v
            d = max(mu_max - mu_min, mv_max - mv_min)
            if best is None or d < best:
                best = d
        return best
