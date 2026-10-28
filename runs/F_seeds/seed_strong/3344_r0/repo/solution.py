from typing import *


class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        n = len(points)
        us = [x + y for x, y in points]
        vs = [x - y for x, y in points]

        def extremes(arr):
            # returns (max1_idx, max1, max2, min1_idx, min1, min2)
            order = sorted(range(n), key=lambda i: arr[i])
            lo1, lo2 = order[0], order[1]
            hi1, hi2 = order[-1], order[-2]
            return hi1, arr[hi1], arr[hi2], lo1, arr[lo1], arr[lo2]

        hi1u, hiu, hiu2, lo1u, lou, lou2 = extremes(us)
        hi1v, hiv, hiv2, lo1v, lov, lov2 = extremes(vs)

        best = None
        for i in range(n):
            if i == hi1u:
                mx_u = hiu2
            else:
                mx_u = hiu
            if i == lo1u:
                mn_u = lou2
            else:
                mn_u = lou
            if i == hi1v:
                mx_v = hiv2
            else:
                mx_v = hiv
            if i == lo1v:
                mn_v = lov2
            else:
                mn_v = lov
            d = max(mx_u - mn_u, mx_v - mn_v)
            if best is None or d < best:
                best = d
        return best
