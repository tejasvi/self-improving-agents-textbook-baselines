from typing import List


class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        n = len(points)
        u = [x + y for x, y in points]
        v = [x - y for x, y in points]

        # Only removing one of the extreme points (top/bottom two in u or v)
        # can reduce the maximum distance; other removals keep it unchanged.
        candidates = set()
        for arr in (u, v):
            order = sorted(range(n), key=arr.__getitem__)
            candidates.update(order[:2])
            candidates.update(order[-2:])

        best = None
        for r in candidates:
            mu_max = mu_min = mv_max = mv_min = None
            for i in range(n):
                if i == r:
                    continue
                a, b = u[i], v[i]
                if mu_max is None:
                    mu_max = mu_min = a
                    mv_max = mv_min = b
                else:
                    if a > mu_max:
                        mu_max = a
                    elif a < mu_min:
                        mu_min = a
                    if b > mv_max:
                        mv_max = b
                    elif b < mv_min:
                        mv_min = b
            d = max(mu_max - mu_min, mv_max - mv_min)
            if best is None or d < best:
                best = d
        return best
