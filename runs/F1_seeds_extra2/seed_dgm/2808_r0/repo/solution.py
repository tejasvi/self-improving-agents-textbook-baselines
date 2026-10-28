from typing import List


class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        n = len(cost)
        INF = float("inf")
        # dp[k] = min cost so that the paid painter's walls cover k walls
        # (capped at n); a paid wall i covers time[i] + 1 walls in total.
        dp = [INF] * (n + 1)
        dp[0] = 0
        for c, t in zip(cost, time):
            step = t + 1
            # Iterate descending so each wall is used at most once.
            for k in range(n, -1, -1):
                if dp[k] == INF:
                    continue
                nk = min(n, k + step)
                if dp[k] + c < dp[nk]:
                    dp[nk] = dp[k] + c
        return dp[n]
