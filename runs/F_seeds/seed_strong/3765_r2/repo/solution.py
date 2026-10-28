from typing import *


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        P = [0] * (n + 1)  # P[j] = nums[0..j-1] sum
        C = [0] * (n + 1)  # C[j] = cost[0..j-1] sum
        for i in range(n):
            P[i + 1] = P[i] + nums[i]
            C[i + 1] = C[i] + cost[i]
        Ctot = C[n]
        INF = float('inf')
        dp = [INF] * (n + 1)
        dp[0] = 0
        # Each segment starting at element i adds k*(Ctot - C[i]) (for the
        # k*index term, summed over elements), plus P_j*(C_j - C_i) for the segment.
        for j in range(1, n + 1):
            pj = P[j]
            best = INF
            for i in range(j):
                v = dp[i] + k * (Ctot - C[i]) - pj * C[i]
                if v < best:
                    best = v
            dp[j] = best + pj * C[j]
        return dp[n]
