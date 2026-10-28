from typing import *


class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        n = len(cost)
        INF = float('inf')
        # dp[j]: min cost so that j walls are covered (capped at n)
        dp = [INF] * (n + 1)
        dp[0] = 0
        for c, t in zip(cost, time):
            step = t + 1
            new = dp[:]
            for j in range(n + 1):
                if dp[j] == INF:
                    continue
                k = min(n, j + step)
                v = dp[j] + c
                if v < new[k]:
                    new[k] = v
            dp = new
        return int(dp[n])
