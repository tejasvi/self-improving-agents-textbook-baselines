from typing import *


class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        n = len(points)
        s = [x + y for x, y in points]
        d = [x - y for x, y in points]
        # Candidates: indices of the 2 smallest and 2 largest of s and d.
        cand = set()
        for arr in (s, d):
            order = sorted(range(n), key=arr.__getitem__)
            cand.update(order[:2])
            cand.update(order[-2:])
        best = None
        for r in cand:
            smax = dmax = -float("inf")
            smin = dmin = float("inf")
            for i in range(n):
                if i == r:
                    continue
                a = s[i]
                b = d[i]
                if a > smax: smax = a
                if a < smin: smin = a
                if b > dmax: dmax = b
                if b < dmin: dmin = b
            val = max(smax - smin, dmax - dmin)
            if best is None or val < best:
                best = val
        return int(best)
