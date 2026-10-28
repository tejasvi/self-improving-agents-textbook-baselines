from typing import List

class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        n = len(cost)
        # Each paid wall contributes (time[i] + 1) units towards covering n walls.
        # We need total contribution >= n with minimum cost.
        # DP over total contribution up to n.
        INF = 10**18
        dp = [INF] * (n + 1)
        dp[0] = 0
        for c, t in zip(cost, time):
            w = t + 1
            # iterate backwards to avoid reuse of same wall multiple times
            new_dp = dp[:]  # copy for this iteration
            for cur in range(n + 1):
                if dp[cur] == INF:
                    continue
                nxt = cur + w
                if nxt > n:
                    nxt = n
                if dp[cur] + c < new_dp[nxt]:
                    new_dp[nxt] = dp[cur] + c
            dp = new_dp
        return dp[n]
