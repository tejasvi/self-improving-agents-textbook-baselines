from typing import List


class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        n = len(cost)
        INF = float("inf")
        # dp[k] = min cost so that at least k walls are painted (capped at n)
        dp = [INF] * (n + 1)
        dp[0] = 0
        for c, t in zip(cost, time):
            gain = t + 1
            for j in range(n, -1, -1):
                if dp[j] == INF:
                    continue
                target = min(n, j + gain)
                if dp[j] + c < dp[target]:
                    dp[target] = dp[j] + c
        return dp[n]
