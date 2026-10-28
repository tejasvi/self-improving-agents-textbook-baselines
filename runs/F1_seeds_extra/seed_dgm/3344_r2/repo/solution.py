from typing import List


class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        n = len(points)
        u = [x + y for x, y in points]
        v = [x - y for x, y in points]

        # Candidate removals: the two largest and two smallest in each of u and v.
        cands = set()
        for arr in (u, v):
            order = sorted(range(n), key=arr.__getitem__)
            cands.update(order[:2])
            cands.update(order[-2:])

        # Top-2 and bottom-2 values with their indices for u and v.
        def extremes(arr):
            order = sorted(range(n), key=arr.__getitem__)
            lo = [(arr[i], i) for i in order[:2]]
            hi = [(arr[i], i) for i in order[-2:]]
            return lo, hi

        ulo, uhi = extremes(u)
        vlo, vhi = extremes(v)

        def spread_without(r, lo, hi):
            # Min and max of arr excluding index r, using the 2 smallest/largest.
            mn = next(val for val, i in lo if i != r)
            mx = next(val for val, i in reversed(hi) if i != r)
            return mx - mn

        best = None
        for r in cands:
            d = max(spread_without(r, ulo, uhi), spread_without(r, vlo, vhi))
            if best is None or d < best:
                best = d
        return best
