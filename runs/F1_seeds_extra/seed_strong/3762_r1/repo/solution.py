from typing import *


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)

        def cost_for_end(x: int, e: int) -> int:
            # Moves needed so each index i gets at least need_i visits,
            # when the walk ends at index e (-1 -> ... -> e).
            # Indices i < e and i == n-1 are visited once by the base walk;
            # indices in (e, n-1) are visited twice (out and back).
            total = n + (n - 1 - e)
            carry = 0
            for i in range(n):
                need = (x + points[i] - 1) // points[i]
                if e == n - 1 or i < e or i == n - 1:
                    base = 1
                else:
                    base = 2
                d = need - base - carry
                if d < 0:
                    d = 0
                total += 2 * d
                carry = d
            return total

        def feasible(x: int) -> bool:
            # Ending at n-1 or n-2 is sufficient (verified against brute force).
            return min(cost_for_end(x, n - 1), cost_for_end(x, n - 2)) <= m

        lo, hi = 0, max(points) * m + 1  # lo feasible, hi infeasible
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid
        return lo
