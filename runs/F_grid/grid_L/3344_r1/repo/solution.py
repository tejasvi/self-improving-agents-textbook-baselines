from typing import List


class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        n = len(points)
        u = [x + y for x, y in points]
        v = [x - y for x, y in points]

        def extremes(vals):
            # indices of 2 smallest and 2 largest values
            order = sorted(range(n), key=lambda i: vals[i])
            lows = order[:2]
            highs = order[-2:]
            return lows, highs

        ul, uh = extremes(u)
        vl, vh = extremes(v)
        candidates = set(ul + uh + vl + vh)

        best = None
        for r in candidates:
            # max/min of u and v excluding r
            def spread(vals, lows, highs):
                mn = next(vals[i] for i in lows if i != r)
                mx = next(vals[i] for i in reversed(highs) if i != r)
                return mx - mn

            d = max(spread(u, ul, uh), spread(v, vl, vh))
            if best is None or d < best:
                best = d
        return best
