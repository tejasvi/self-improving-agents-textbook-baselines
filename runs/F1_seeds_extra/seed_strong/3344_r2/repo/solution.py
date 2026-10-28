from typing import *


class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        n = len(points)
        s = [x + y for x, y in points]
        d = [x - y for x, y in points]
        # Candidate removals: argmax/argmin of s and d.
        cands = {s.index(max(s)), s.index(min(s)), d.index(max(d)), d.index(min(d))}

        def dist_without(skip: int) -> int:
            hi_s = lo_s = hi_d = lo_d = None
            for i in range(n):
                if i == skip:
                    continue
                a = s[i]
                b = d[i]
                if hi_s is None:
                    hi_s = lo_s = a
                    hi_d = lo_d = b
                else:
                    if a > hi_s: hi_s = a
                    if a < lo_s: lo_s = a
                    if b > hi_d: hi_d = b
                    if b < lo_d: lo_d = b
            return max(hi_s - lo_s, hi_d - lo_d)

        return min(dist_without(c) for c in cands)
