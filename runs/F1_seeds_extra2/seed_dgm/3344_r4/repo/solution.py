from typing import List


class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        n = len(points)
        u = [x + y for x, y in points]
        v = [x - y for x, y in points]

        def ranks(vals):
            order = sorted(range(n), key=lambda i: vals[i])
            pos = [0] * n
            for p, i in enumerate(order):
                pos[i] = p
            return order, pos

        ou, pu = ranks(u)
        ov, pv = ranks(v)

        best = float("inf")
        for i in range(n):
            # range of u excluding i
            if pu[i] == n - 1:
                maxu = u[ou[n - 2]]
            else:
                maxu = u[ou[n - 1]]
            if pu[i] == 0:
                minu = u[ou[1]]
            else:
                minu = u[ou[0]]
            # range of v excluding i
            if pv[i] == n - 1:
                maxv = v[ov[n - 2]]
            else:
                maxv = v[ov[n - 1]]
            if pv[i] == 0:
                minv = v[ov[1]]
            else:
                minv = v[ov[0]]
            best = min(best, max(maxu - minu, maxv - minv))
        return best
