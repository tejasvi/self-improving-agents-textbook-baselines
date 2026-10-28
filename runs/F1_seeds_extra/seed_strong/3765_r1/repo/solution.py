from typing import *


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # 1-indexed prefix sums
        Pn = [0] * (n + 1)
        Cn = [0] * (n + 1)
        for i in range(n):
            Pn[i + 1] = Pn[i] + nums[i]
            Cn[i + 1] = Cn[i] + cost[i]
        Ctot = Cn[n]
        # Segment (j, i] costs Pn[i]*(Cn[i]-Cn[j]) + k*(Ctot - Cn[j]) in the
        # reformulated (index-free) cost, since sum_t S_t * t = sum_t sum_{s>=t} S_s.
        INF = float('inf')
        dp = [INF] * (n + 1)
        dp[0] = 0
        for i in range(1, n + 1):
            p = Pn[i]
            ci = Cn[i]
            best = INF
            for j in range(i):
                cj = Cn[j]
                v = dp[j] + p * (ci - cj) + k * (Ctot - cj)
                if v < best:
                    best = v
            dp[i] = best
        return dp[n]
