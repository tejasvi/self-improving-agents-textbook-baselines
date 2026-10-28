from typing import *


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)

        def check(x: int) -> bool:
            # Minimum arrivals needed at each cell to reach score x.
            need = [-(-x // p) for p in points]
            # Weight arrays for the covering problem over edges.
            A = [v - 1 if v > 1 else 0 for v in need]
            B = [0] * n
            for i in range(n):
                w = need[i] - 1
                if i < n - 1:
                    w -= 1
                B[i] = w if w > 0 else 0
            # P[i] = max weight independent set of A[0..i-1]
            P = [0] * (n + 1)
            take = 0
            skip = 0
            for i in range(n):
                take, skip = skip + A[i], (take if take > skip else skip)
                P[i + 1] = take if take > skip else skip
            # S[i] = max weight independent set of B[i..n-1]
            S = [0] * (n + 2)
            take = 0
            skip = 0
            for i in range(n - 1, -1, -1):
                take, skip = skip + B[i], (take if take > skip else skip)
                S[i] = take if take > skip else skip
            for q in range(n):
                v = need[q] - 1
                if q < n - 1:
                    v -= 1
                cq = v if v > 0 else 0
                t = P[q - 1 if q >= 1 else 0] + cq + S[min(q + 2, n)]
                s = P[q] + S[q + 1]
                sq = t if t > s else s
                cost = 2 * n - 1 - q + 2 * sq
                if cost <= m:
                    return True
            return False

        lo, hi = 0, max(points) * (m + 1)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if check(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
