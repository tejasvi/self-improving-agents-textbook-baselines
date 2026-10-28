from typing import *


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        # Edge j (between cells j and j+1, j = -1..n-2) is traversed t_j times.
        # Parity: t_j odd iff j < e (final index e); t_j >= 1 for all j (all cells visited).
        # Cell i gets visits (t_{i-1} + t_i + [i == e]) / 2, which must be >= ceil(X / points[i]).
        # Ending at e = n-2 or n-1 is always optimal (verified by brute force).

        def cost(X: int, e: int) -> int:
            # T[k] = t_{k-1}, k = 0..n-1 ; T[n] (nonexistent edge) = 0
            lo = [1 if k <= e else 2 for k in range(n)]
            T = lo[:]
            total_extra = 0
            for i in range(n):
                c = -(-X // points[i])
                D = 2 * c - (1 if i == e else 0)
                if i + 1 == n:
                    need = D - T[i]
                    if need > 0:
                        v = T[i] + need
                        if (v - lo[i]) % 2:
                            v += 1
                        T[i] = v
                    break
                need = D - T[i]
                v = lo[i + 1] if lo[i + 1] > need else need
                if (v - lo[i + 1]) % 2:
                    v += 1
                T[i + 1] = v
            return sum(T)

        def feasible(X: int) -> bool:
            for e in (n - 2, n - 1):
                if cost(X, e) <= m:
                    return True
            return False

        lo, hi = 0, max(points) * m
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
