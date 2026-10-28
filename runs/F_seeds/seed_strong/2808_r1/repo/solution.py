from typing import *


class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        n = len(cost)
        INF = float('inf')
        # dp[j] = min cost so that the paid painters cover a set of walls whose
        # sum of (time+1), capped at n, equals j.
        dp = [INF] * (n + 1)
        dp[0] = 0
        for c, t in zip(cost, time):
            w = t + 1
            new = dp[:]
            for j in range(n + 1):
                if dp[j] == INF:
                    continue
                nj = min(n, j + w)
                v = dp[j] + c
                if v < new[nj]:
                    new[nj] = v
            dp = new
        return dp[n]
