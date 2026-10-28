from typing import *


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # Pn[r]: prefix sum of nums up to index r-1 (length r)
        # Cp[r]: prefix sum of cost up to index r-1
        Pn = [0] * (n + 1)
        Cp = [0] * (n + 1)
        for i in range(n):
            Pn[i + 1] = Pn[i] + nums[i]
            Cp[i + 1] = Cp[i] + cost[i]
        ctot = Cp[n]
        # Each segment starting at l contributes k*(ctot - Cp[l]) independent of its index.
        # dp[r] = min over l < r of dp[l] + Pn[r]*(Cp[r]-Cp[l]) + k*(ctot-Cp[l])
        INF = float("inf")
        dp = [INF] * (n + 1)
        dp[0] = 0
        for r in range(1, n + 1):
            pr = Pn[r]
            cr = Cp[r]
            best = INF
            for l in range(r):
                v = dp[l] + pr * (cr - Cp[l]) + k * (ctot - Cp[l])
                if v < best:
                    best = v
            dp[r] = best
        return int(dp[n])
