from typing import List


class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        n = len(points)
        u = [x + y for x, y in points]
        v = [x - y for x, y in points]

        def diameter_excluding(skip: int) -> int:
            umax = umin = vmax = vmin = None
            for i in range(n):
                if i == skip:
                    continue
                a = u[i]
                b = v[i]
                if umax is None:
                    umax = umin = a
                    vmax = vmin = b
                else:
                    if a > umax:
                        umax = a
                    elif a < umin:
                        umin = a
                    if b > vmax:
                        vmax = b
                    elif b < vmin:
                        vmin = b
            return max(umax - umin, vmax - vmin)

        # Only extreme points can change the diameter when removed.
        candidates = {
            u.index(max(u)), u.index(min(u)),
            v.index(max(v)), v.index(min(v)),
        }
        best = min(diameter_excluding(i) for i in candidates)
        if len(candidates) < n:
            # some non-extreme point exists; removing it keeps the full diameter
            best = min(best, diameter_excluding(-1))
        return best
