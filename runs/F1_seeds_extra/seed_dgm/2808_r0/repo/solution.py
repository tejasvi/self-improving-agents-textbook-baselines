from typing import List


class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        n = len(cost)
        INF = float("inf")
        # dp[k] = min cost to have k walls painted (capped at n)
        dp = [INF] * (n + 1)
        dp[0] = 0
        for i in range(n):
            gain = time[i] + 1
            c = cost[i]
            for k in range(n, -1, -1):
                if dp[k] == INF:
                    continue
                t = min(n, k + gain)
                if dp[k] + c < dp[t]:
                    dp[t] = dp[k] + c
        return dp[n]
