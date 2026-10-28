from typing import List


class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        n = len(points)
        us = [x + y for x, y in points]
        vs = [x - y for x, y in points]

        def top_bottom(vals):
            # indices of two largest and two smallest values
            order = sorted(range(n), key=vals.__getitem__)
            lo = order[:2]  # smallest two (lo[0] is global min)
            hi = order[-2:][::-1]  # largest two (hi[0] is global max)
            return lo, hi

        ulo, uhi = top_bottom(us)
        vlo, vhi = top_bottom(vs)

        def range_without(vals, lo, hi, i):
            # max - min of vals excluding index i (n >= 3 so at least 2 remain)
            mx = vals[hi[1]] if hi[0] == i else vals[hi[0]]
            mn = vals[lo[1]] if lo[0] == i else vals[lo[0]]
            return mx - mn

        best = None
        for i in range(n):
            d = max(range_without(us, ulo, uhi, i), range_without(vs, vlo, vhi, i))
            if best is None or d < best:
                best = d
        return best
