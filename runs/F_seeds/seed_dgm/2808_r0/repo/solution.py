from typing import List


class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        n = len(cost)
        INF = float("inf")
        # dp[k] = min paid cost so that k walls are covered (capped at n)
        dp = [INF] * (n + 1)
        dp[0] = 0
        for c, t in zip(cost, time):
            new = dp[:]
            step = t + 1
            for k in range(n + 1):
                if dp[k] == INF:
                    continue
                nk = min(n, k + step)
                v = dp[k] + c
                if v < new[nk]:
                    new[nk] = v
            dp = new
        return int(dp[n])
