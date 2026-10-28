from typing import List


class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        n = len(points)
        us = [x + y for x, y in points]
        vs = [x - y for x, y in points]

        # Removing a point that is not an extreme in u or v cannot reduce
        # the diameter, so only the top/bottom 2 indices per coordinate matter.
        cand = set()
        for arr in (us, vs):
            order = sorted(range(n), key=arr.__getitem__)
            cand.update(order[:2])
            cand.update(order[-2:])

        best = None
        for c in cand:
            mnu = mxu = mnv = mxv = None
            for i in range(n):
                if i == c:
                    continue
                u = us[i]
                v = vs[i]
                if mnu is None:
                    mnu = mxu = u
                    mnv = mxv = v
                else:
                    if u < mnu:
                        mnu = u
                    elif u > mxu:
                        mxu = u
                    if v < mnv:
                        mnv = v
                    elif v > mxv:
                        mxv = v
            d = max(mxu - mnu, mxv - mnv)
            if best is None or d < best:
                best = d
        return best
