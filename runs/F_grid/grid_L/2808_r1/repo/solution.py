from typing import List


class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        n = len(cost)
        INF = float("inf")
        # dp[j] = min cost so that j walls are covered (capped at n)
        dp = [INF] * (n + 1)
        dp[0] = 0
        for c, t in zip(cost, time):
            new = dp[:]
            gain = t + 1  # this paid wall plus t walls painted by the free painter
            for j in range(n + 1):
                if dp[j] == INF:
                    continue
                k = min(n, j + gain)
                if dp[j] + c < new[k]:
                    new[k] = dp[j] + c
            dp = new
        return int(dp[n])
