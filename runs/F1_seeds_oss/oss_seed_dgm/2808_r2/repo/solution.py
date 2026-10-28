from typing import List

class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        n = len(cost)
        # Each wall painted by paid painter contributes (time[i] + 1) towards the requirement
        # because we get 1 extra wall (the paid wall itself) plus the time during which
        # the free painter can paint other walls (1 wall per unit time).
        # We need total contribution >= n.
        target = n
        INF = 10**18
        # dp[v] = minimal cost to achieve total contribution exactly v (capped at target)
        dp = [INF] * (target + 1)
        dp[0] = 0
        for c, t in zip(cost, time):
            v = t + 1
            # iterate backwards to avoid reuse within same iteration
            for cur in range(target, -1, -1):
                if dp[cur] == INF:
                    continue
                nxt = cur + v
                if nxt > target:
                    nxt = target
                if dp[nxt] > dp[cur] + c:
                    dp[nxt] = dp[cur] + c
        return dp[target]
