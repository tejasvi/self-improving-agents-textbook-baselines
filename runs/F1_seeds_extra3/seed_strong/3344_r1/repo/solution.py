from typing import *


class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        n = len(points)
        s = [x + y for x, y in points]
        d = [x - y for x, y in points]
        # Removing a non-extreme point cannot reduce the diameter, so only
        # the extreme points (argmax/argmin of s and d) need to be tried.
        cands = {s.index(max(s)), s.index(min(s)), d.index(max(d)), d.index(min(d))}
        best = None
        for c in cands:
            mxs = mns = mxd = mnd = None
            for i in range(n):
                if i == c:
                    continue
                a = s[i]
                b = d[i]
                if mxs is None:
                    mxs = mns = a
                    mxd = mnd = b
                else:
                    if a > mxs: mxs = a
                    if a < mns: mns = a
                    if b > mxd: mxd = b
                    if b < mnd: mnd = b
            r = max(mxs - mns, mxd - mnd)
            if best is None or r < best:
                best = r
        return best
