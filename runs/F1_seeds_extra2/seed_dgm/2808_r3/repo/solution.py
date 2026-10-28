from typing import List


class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        n = len(cost)
        INF = float("inf")
        # dp[k] = min cost so that k walls are covered (capped at n)
        dp = [INF] * (n + 1)
        dp[0] = 0
        for c, t in zip(cost, time):
            gain = t + 1
            new = dp[:]
            for k in range(n + 1):
                if dp[k] == INF:
                    continue
                nk = min(n, k + gain)
                if dp[k] + c < new[nk]:
                    new[nk] = dp[k] + c
            dp = new
        return int(dp[n])
