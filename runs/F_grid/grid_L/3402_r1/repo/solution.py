from typing import List


class Solution:
    def minCostToEqualizeArray(self, nums: List[int], cost1: int, cost2: int) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        if n == 1:
            return 0
        M = max(nums)
        mn = min(nums)
        total = sum(nums)
        use_pairs = cost2 < 2 * cost1
        best = None
        # Beyond roughly 2*M the cost is governed by a simple linear/parity
        # pattern, so a bounded scan over the target value is sufficient.
        limit = M + 2 * M + 5
        for T in range(M, limit + 1):
            S = n * T - total
            m = T - mn
            if use_pairs:
                if 2 * m <= S:
                    k = S // 2
                else:
                    k = S - m
                cost = k * cost2 + (S - 2 * k) * cost1
            else:
                cost = S * cost1
            if best is None or cost < best:
                best = cost
        return best % MOD
