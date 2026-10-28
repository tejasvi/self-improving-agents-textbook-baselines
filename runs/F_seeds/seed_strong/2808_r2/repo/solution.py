from typing import *


class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        n = len(cost)
        INF = float('inf')
        # dp[k] = min cost so that k walls are covered (capped at n)
        dp = [INF] * (n + 1)
        dp[0] = 0
        for i in range(n):
            c = cost[i]
            gain = time[i] + 1
            new = dp[:]
            for j in range(n + 1):
                if dp[j] == INF:
                    continue
                t = j + gain
                if t > n:
                    t = n
                v = dp[j] + c
                if v < new[t]:
                    new[t] = v
            dp = new
        return int(dp[n])
