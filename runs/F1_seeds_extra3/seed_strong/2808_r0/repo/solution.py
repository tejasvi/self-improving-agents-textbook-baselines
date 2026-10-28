from typing import *


class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        n = len(cost)
        INF = float('inf')
        # dp[j] = min cost so that at least j walls are painted (capped at n)
        dp = [INF] * (n + 1)
        dp[0] = 0
        for i in range(n):
            c = cost[i]
            span = time[i] + 1
            for j in range(n, -1, -1):
                if dp[j] == INF:
                    continue
                k = j + span
                if k > n:
                    k = n
                v = dp[j] + c
                if v < dp[k]:
                    dp[k] = v
        return int(dp[n])
