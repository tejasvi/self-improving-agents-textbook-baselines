from typing import *


class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        n = len(points)
        # s = x + y, d = x - y; Manhattan distance = max(|ds|, |dd|) over pairs.
        s = [x + y for x, y in points]
        d = [x - y for x, y in points]

        def top2(vals, largest):
            # Returns [(value, index), (value, index)] of two most extreme entries.
            best = [None, None]
            for i, v in enumerate(vals):
                if largest:
                    if best[0] is None or v > best[0][0]:
                        best[1] = best[0]
                        best[0] = (v, i)
                    elif best[1] is None or v > best[1][0]:
                        best[1] = (v, i)
                else:
                    if best[0] is None or v < best[0][0]:
                        best[1] = best[0]
                        best[0] = (v, i)
                    elif best[1] is None or v < best[1][0]:
                        best[1] = (v, i)
            return best

        smax = top2(s, True)
        smin = top2(s, False)
        dmax = top2(d, True)
        dmin = top2(d, False)

        def pick(pair, i):
            # value of the extreme after removing index i
            return pair[1][0] if pair[0][1] == i else pair[0][0]

        ans = None
        for i in range(n):
            hi_s = pick(smax, i)
            lo_s = pick(smin, i)
            hi_d = pick(dmax, i)
            lo_d = pick(dmin, i)
            cur = max(hi_s - lo_s, hi_d - lo_d)
            if ans is None or cur < ans:
                ans = cur
        return ans
