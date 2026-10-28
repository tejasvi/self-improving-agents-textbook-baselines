from typing import List


class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        n = len(points)
        us = [x + y for x, y in points]
        vs = [x - y for x, y in points]

        def top_bottom(vals):
            order = sorted(range(n), key=lambda i: vals[i])
            # two smallest and two largest indices
            lo = order[:2]
            hi = order[-2:][::-1]
            return lo, hi

        ulo, uhi = top_bottom(us)
        vlo, vhi = top_bottom(vs)

        def range_without(i, vals, lo, hi):
            # lo: indices of smallest (ascending), hi: indices of largest (descending)
            remaining_min = None
            for j in lo:
                if j != i:
                    remaining_min = vals[j]
                    break
            remaining_max = None
            for j in hi:
                if j != i:
                    remaining_max = vals[j]
                    break
            return remaining_max - remaining_min

        best = None
        for i in range(n):
            d = max(
                range_without(i, us, ulo, uhi),
                range_without(i, vs, vlo, vhi),
            )
            if best is None or d < best:
                best = d
        return best
