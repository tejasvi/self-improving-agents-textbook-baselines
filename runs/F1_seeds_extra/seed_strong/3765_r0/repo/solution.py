from typing import *


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        # Let P[j], C[j] be prefix sums of nums and cost (length j).
        # Total cost = sum over segments (i, j] of
        #   P[j]*(C[j]-C[i]) + k*(C[n]-C[i]),
        # since sum_t t*Cseg_t = sum_u (C[n] - C[start_u]).
        n = len(nums)
        P = [0] * (n + 1)
        C = [0] * (n + 1)
        for idx in range(n):
            P[idx + 1] = P[idx] + nums[idx]
            C[idx + 1] = C[idx] + cost[idx]
        Cn = C[n]
        INF = float("inf")
        dp = [INF] * (n + 1)
        dp[0] = 0
        for j in range(1, n + 1):
            pj = P[j]
            best = INF
            for i in range(j):
                v = dp[i] + pj * (C[j] - C[i]) + k * (Cn - C[i])
                if v < best:
                    best = v
            dp[j] = best
        return int(dp[n])
