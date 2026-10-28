from typing import List


class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        n = len(points)
        us = [x + y for x, y in points]
        vs = [x - y for x, y in points]

        # Candidates: points holding the 2 largest / 2 smallest u or v values.
        # Removing any other point leaves the diameter unchanged, which is never
        # better than removing one of these extremes.
        cand = set()
        for arr in (us, vs):
            order = sorted(range(n), key=arr.__getitem__)
            cand.update(order[:2])
            cand.update(order[-2:])

        best = None
        for c in cand:
            min_u = min_v = float("inf")
            max_u = max_v = float("-inf")
            for i in range(n):
                if i == c:
                    continue
                u = us[i]
                v = vs[i]
                if u < min_u:
                    min_u = u
                if u > max_u:
                    max_u = u
                if v < min_v:
                    min_v = v
                if v > max_v:
                    max_v = v
            d = max(max_u - min_u, max_v - min_v)
            if best is None or d < best:
                best = d
        return int(best)
