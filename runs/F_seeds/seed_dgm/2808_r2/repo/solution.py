from typing import List


class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        n = len(cost)
        INF = float("inf")
        # dp[j] = min cost so that j walls (capped at n) are covered by paid painter
        dp = [INF] * (n + 1)
        dp[0] = 0
        for i in range(n):
            c = cost[i]
            span = time[i] + 1
            new = dp[:]
            for j in range(n + 1):
                if dp[j] == INF:
                    continue
                k = min(n, j + span)
                v = dp[j] + c
                if v < new[k]:
                    new[k] = v
            dp = new
        return dp[n]
