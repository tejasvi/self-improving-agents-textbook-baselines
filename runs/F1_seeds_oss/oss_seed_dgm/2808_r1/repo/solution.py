from typing import List

class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        n = len(cost)
        # Each paid wall contributes its painting plus time_i units during which free painter can paint
        # So the total number of walls that can be covered by a subset S is sum(time_i) + len(S)
        # We need this total to be at least n.
        # DP: dp[v] = minimum cost to achieve total coverage v (capped at n)
        INF = 10**18
        dp = [INF] * (n + 1)
        dp[0] = 0
        for c, t in zip(cost, time):
            value = t + 1  # coverage contributed by this wall if paid
            ndp = dp[:]  # copy for iteration to avoid reuse within same iteration
            for v in range(n + 1):
                if dp[v] == INF:
                    continue
                new_v = v + value
                if new_v > n:
                    new_v = n
                if ndp[new_v] > dp[v] + c:
                    ndp[new_v] = dp[v] + c
            dp = ndp
        return dp[n]
