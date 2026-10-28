from typing import List

class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        n = len(cost)
        # each selected wall contributes (time[i] + 1) towards the required "busy time + wall count" value
        # we need total contribution >= n with minimal cost
        INF = 10**18
        dp = [INF] * (n + 1)
        dp[0] = 0
        for c, t in zip(cost, time):
            val = t + 1
            # iterate backwards to avoid reuse of same wall multiple times
            for cur in range(n, -1, -1):
                if dp[cur] == INF:
                    continue
                nxt = cur + val
                if nxt > n:
                    nxt = n
                if dp[nxt] > dp[cur] + c:
                    dp[nxt] = dp[cur] + c
        return dp[n]
