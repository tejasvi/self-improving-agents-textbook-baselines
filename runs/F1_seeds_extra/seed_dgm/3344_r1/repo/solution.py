from typing import List


class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        n = len(points)
        us = [x + y for x, y in points]
        vs = [x - y for x, y in points]

        def diameter(skip: int) -> int:
            umax = -float("inf")
            umin = float("inf")
            vmax = -float("inf")
            vmin = float("inf")
            for i in range(n):
                if i == skip:
                    continue
                u = us[i]
                v = vs[i]
                if u > umax:
                    umax = u
                if u < umin:
                    umin = u
                if v > vmax:
                    vmax = v
                if v < vmin:
                    vmin = v
            return int(max(umax - umin, vmax - vmin))

        # Candidate indices: top-2 and bottom-2 of u and of v.
        candidates = set()
        for arr in (us, vs):
            order = sorted(range(n), key=lambda i: arr[i])
            candidates.update(order[:2])
            candidates.update(order[-2:])

        best = diameter(-1)  # removing a non-extreme point keeps this value
        for c in candidates:
            best = min(best, diameter(c))
        return best
