from typing import List


class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        n = len(cost)
        INF = float("inf")
        # dp[j] = min cost so that j walls (capped at n) are painted
        dp = [INF] * (n + 1)
        dp[0] = 0
        for c, t in zip(cost, time):
            gain = t + 1
            for j in range(n, -1, -1):
                if dp[j] == INF:
                    continue
                k = min(n, j + gain)
                if dp[j] + c < dp[k]:
                    dp[k] = dp[j] + c
        return int(dp[n])
