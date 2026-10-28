from typing import List


class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        n = len(points)
        u = [x + y for x, y in points]
        v = [x - y for x, y in points]

        def extremes(vals):
            order = sorted(range(n), key=lambda i: vals[i])
            # smallest and second smallest, largest and second largest indices
            return order[0], order[1], order[-1], order[-2]

        umin1, umin2, umax1, umax2 = extremes(u)
        vmin1, vmin2, vmax1, vmax2 = extremes(v)

        best = None
        for i in range(n):
            if i == umax1:
                hi_u = u[umax2]
            else:
                hi_u = u[umax1]
            if i == umin1:
                lo_u = u[umin2]
            else:
                lo_u = u[umin1]
            if i == vmax1:
                hi_v = v[vmax2]
            else:
                hi_v = v[vmax1]
            if i == vmin1:
                lo_v = v[vmin2]
            else:
                lo_v = v[vmin1]
            d = max(hi_u - lo_u, hi_v - lo_v)
            if best is None or d < best:
                best = d
        return best
