from typing import *


class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        n = len(points)
        u = [x + y for x, y in points]
        v = [x - y for x, y in points]
        iu = sorted(range(n), key=lambda i: u[i])
        iv = sorted(range(n), key=lambda i: v[i])
        # indices of extremes
        umin_i, umin2_i = iu[0], iu[1]
        umax_i, umax2_i = iu[-1], iu[-2]
        vmin_i, vmin2_i = iv[0], iv[1]
        vmax_i, vmax2_i = iv[-1], iv[-2]
        best = None
        for i in range(n):
            if i == umax_i:
                mx = u[umax2_i]
            else:
                mx = u[umax_i]
            if i == umin_i:
                mn = u[umin2_i]
            else:
                mn = u[umin_i]
            if i == vmax_i:
                mxv = v[vmax2_i]
            else:
                mxv = v[vmax_i]
            if i == vmin_i:
                mnv = v[vmin2_i]
            else:
                mnv = v[vmin_i]
            d = max(mx - mn, mxv - mnv)
            if best is None or d < best:
                best = d
        return best
