from typing import List

class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        n = len(cost)
        # Each wall assigned to paid painter contributes weight = time[i] + 1.
        # Need total weight >= n to allow free painter to paint remaining walls.
        max_weight = n + max(time) + 1  # upper bound for DP array size
        INF = 10**18
        dp = [INF] * (max_weight + 1)
        dp[0] = 0
        for c, t in zip(cost, time):
            w = t + 1
            # iterate backwards to avoid reuse of same wall multiple times
            for cur in range(max_weight, -1, -1):
                if dp[cur] == INF:
                    continue
                nxt = cur + w
                if nxt > max_weight:
                    nxt = max_weight
                if dp[nxt] > dp[cur] + c:
                    dp[nxt] = dp[cur] + c
        # answer is minimal cost for total weight >= n
        answer = min(dp[n:])
        return answer
