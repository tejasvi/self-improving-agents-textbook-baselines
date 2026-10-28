from typing import List


class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        n = len(points)
        # Manhattan distance = max(|du|, |dv|) with u = x+y, v = x-y.
        u = [x + y for x, y in points]
        v = [x - y for x, y in points]

        def spread_without(vals, skip):
            lo = min(vals[i] for i in range(n) if i != skip)
            hi = max(vals[i] for i in range(n) if i != skip)
            return hi - lo

        # Removing a non-extreme point leaves the full spread (an upper bound
        # that the extremes already achieve or beat), so only extremes matter.
        candidates = set()
        for vals in (u, v):
            order = sorted(range(n), key=lambda i: vals[i])
            candidates.update(order[:2])
            candidates.update(order[-2:])

        return min(
            max(spread_without(u, c), spread_without(v, c)) for c in candidates
        )
