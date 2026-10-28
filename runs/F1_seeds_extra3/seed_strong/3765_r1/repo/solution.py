from typing import *


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # P[i]: sum of nums[0..i-1]; C[i]: sum of cost[0..i-1]
        P = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            P[i + 1] = P[i] + nums[i]
            C[i + 1] = C[i] + cost[i]
        # Segment t's k*t*cost term rewritten as k * (suffix cost from its start),
        # so each segment [j, i) contributes P[i]*(C[i]-C[j]) + k*(C[n]-C[j]).
        INF = float('inf')
        dp = [INF] * (n + 1)
        dp[0] = 0
        Cn = C[n]
        for i in range(1, n + 1):
            pi = P[i]
            ci = C[i]
            best = INF
            for j in range(i):
                v = dp[j] + pi * (ci - C[j]) + k * (Cn - C[j])
                if v < best:
                    best = v
            dp[i] = best
        return int(dp[n])
