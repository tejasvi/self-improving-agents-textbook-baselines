from typing import List


class Solution:
    def minCostToEqualizeArray(self, nums: List[int], cost1: int, cost2: int) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        mx = max(nums)
        mn = min(nums)
        total = sum(nums)

        def cost_for(T: int) -> int:
            S = n * T - total          # total increments needed
            M = T - mn                 # largest single deficit
            # Pairs p: p <= S - M (partners for the max element) and 2p <= S.
            pmax = min(S - M, S // 2)
            p = pmax if cost2 < 2 * cost1 else 0
            return p * cost2 + (S - 2 * p) * cost1

        candidates = {mx, mx + 1, mx + 2}
        if n > 2:
            # Regime boundary: 2*(T - mn) = n*T - total  ->  T = (total - 2*mn) / (n - 2)
            t0 = (total - 2 * mn) // (n - 2)
            for t in range(t0 - 2, t0 + 3):
                candidates.add(t)
        candidates = [t for t in candidates if t >= mx]
        best = min(cost_for(T) for T in candidates)
        return best % MOD
