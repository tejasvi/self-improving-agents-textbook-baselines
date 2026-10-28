from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # P[j] = sum of nums[0..j-1], Q[j] = sum of cost[0..j-1]
        P = [0] * (n + 1)
        Q = [0] * (n + 1)
        for idx in range(n):
            P[idx + 1] = P[idx] + nums[idx]
            Q[idx + 1] = Q[idx] + cost[idx]
        total = Q[n]
        # A segment covering [i, j) costs P[j]*(Q[j]-Q[i]) + k*(total-Q[i]);
        # the k*index term is folded into the suffix sums of segment costs.
        INF = float("inf")
        dp = [INF] * (n + 1)
        dp[0] = 0
        for j in range(1, n + 1):
            best = INF
            pj = P[j]
            qj = Q[j]
            for i in range(j):
                val = dp[i] + pj * (qj - Q[i]) + k * (total - Q[i])
                if val < best:
                    best = val
            dp[j] = best
        return int(dp[n])
