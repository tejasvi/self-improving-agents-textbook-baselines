from typing import List
import heapq


class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        n = len(points)
        u = [x + y for x, y in points]
        v = [x - y for x, y in points]

        # Candidates: points that determine the extremes of u or v.
        cands = set()
        for arr in (u, v):
            order = sorted(range(n), key=lambda i: arr[i])
            cands.update(order[:2])
            cands.update(order[-2:])

        best = None
        for r in cands:
            mnu = mxu = mnv = mxv = None
            for i in range(n):
                if i == r:
                    continue
                a, b = u[i], v[i]
                if mnu is None:
                    mnu = mxu = a
                    mnv = mxv = b
                else:
                    if a < mnu:
                        mnu = a
                    elif a > mxu:
                        mxu = a
                    if b < mnv:
                        mnv = b
                    elif b > mxv:
                        mxv = b
            d = max(mxu - mnu, mxv - mnv)
            if best is None or d < best:
                best = d
        return best
