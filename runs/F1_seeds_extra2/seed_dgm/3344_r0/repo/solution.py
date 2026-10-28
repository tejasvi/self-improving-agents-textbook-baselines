from typing import List


class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        n = len(points)
        us = [x + y for x, y in points]
        vs = [x - y for x, y in points]

        # Candidates: indices of the 2 largest and 2 smallest values of u and v.
        # Removing any other point leaves the extremes intact, so the answer
        # is never better than removing a candidate.
        cands = set()
        for arr in (us, vs):
            order = sorted(range(n), key=arr.__getitem__)
            cands.update(order[:2])
            cands.update(order[-2:])

        best = None
        for c in cands:
            maxu = minu = maxv = minv = None
            for i in range(n):
                if i == c:
                    continue
                u = us[i]
                v = vs[i]
                if maxu is None:
                    maxu = minu = u
                    maxv = minv = v
                else:
                    if u > maxu:
                        maxu = u
                    elif u < minu:
                        minu = u
                    if v > maxv:
                        maxv = v
                    elif v < minv:
                        minv = v
            d = max(maxu - minu, maxv - minv)
            if best is None or d < best:
                best = d
        return best
