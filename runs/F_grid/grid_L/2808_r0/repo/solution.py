from typing import List


class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        n = len(cost)
        INF = float("inf")
        # dp[j] = min cost so that j walls are covered (capped at n)
        dp = [INF] * (n + 1)
        dp[0] = 0
        for c, t in zip(cost, time):
            w = t + 1  # paid wall covers itself plus t free-painter walls
            for j in range(n, -1, -1):
                if dp[j] == INF:
                    continue
                nj = min(n, j + w)
                if dp[j] + c < dp[nj]:
                    dp[nj] = dp[j] + c
        return int(dp[n])
