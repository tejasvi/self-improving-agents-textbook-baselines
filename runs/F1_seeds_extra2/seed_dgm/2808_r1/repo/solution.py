from typing import List


class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        n = len(cost)
        INF = float("inf")
        # dp[k] = min cost of paid walls covering k walls (capped at n)
        dp = [INF] * (n + 1)
        dp[0] = 0
        for c, t in zip(cost, time):
            gain = t + 1
            for k in range(n, 0, -1):
                prev = max(0, k - gain)
                if dp[prev] + c < dp[k]:
                    dp[k] = dp[prev] + c
        return int(dp[n])
