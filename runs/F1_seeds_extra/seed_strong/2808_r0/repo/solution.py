from typing import *


class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        n = len(cost)
        INF = float('inf')
        # dp[k] = min cost so that walls covered (paid time + free) is k, capped at n
        dp = [INF] * (n + 1)
        dp[0] = 0
        for i in range(n):
            c = cost[i]
            gain = time[i] + 1
            new = dp[:]
            for k in range(n + 1):
                if dp[k] == INF:
                    continue
                nk = min(n, k + gain)
                v = dp[k] + c
                if v < new[nk]:
                    new[nk] = v
            dp = new
        return dp[n]
