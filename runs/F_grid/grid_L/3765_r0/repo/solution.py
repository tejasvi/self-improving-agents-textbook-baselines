from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # P[i]: prefix sum of nums, C[i]: prefix sum of cost (1-indexed, P[0]=C[0]=0)
        P = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            P[i + 1] = P[i] + nums[i]
            C[i + 1] = C[i] + cost[i]
        # The k*i term summed over subarrays equals k * sum_u (C[n] - C[l_u - 1]),
        # so each subarray (j, i] costs P[i]*(C[i]-C[j]) + k*(C[n]-C[j]).
        INF = float("inf")
        dp = [INF] * (n + 1)
        dp[0] = 0
        for i in range(1, n + 1):
            best = INF
            for j in range(i):
                val = dp[j] + P[i] * (C[i] - C[j]) + k * (C[n] - C[j])
                if val < best:
                    best = val
            dp[i] = best
        return dp[n]
