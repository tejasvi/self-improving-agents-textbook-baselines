from typing import List


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        NEG = -(1 << 62)

        def feasible(k: int) -> bool:
            # Cells needing visits; a cell visited by the base walk once/twice
            # needs the remaining visits from back-and-forth bounces, which
            # cover adjacent pairs (a path), solved as max-weight independent set.
            need = [-(-k // p) for p in points]
            w1 = [max(0, need[i] - 1) for i in range(n)]
            w2 = [max(0, need[i] - 2) if i <= n - 2 else w1[i] for i in range(n)]

            # Suffix DP with base-2 weights for cells e..n-1.
            Sa = [0] * (n + 1)
            Sb = [NEG] * (n + 1)
            for i in range(n - 1, -1, -1):
                Sa[i] = max(Sa[i + 1], Sb[i + 1])
                Sb[i] = w2[i] + Sa[i + 1]

            # Prefix DP with base-1 weights for cells 0..e-1.
            pa, pb = 0, NEG
            for e in range(n):
                tot = max(pa + Sb[e], max(pa, pb) + Sa[e])
                cost = (2 * n - 1 - e) + 2 * tot
                if cost <= m:
                    return True
                pa, pb = max(pa, pb), pa + w1[e]
            return False

        lo, hi = 0, max(points) * (m + 1)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
