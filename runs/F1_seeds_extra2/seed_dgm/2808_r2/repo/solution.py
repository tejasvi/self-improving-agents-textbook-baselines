from typing import List


class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        n = len(cost)
        INF = float('inf')
        # dp[r + n] = min cost, where r = (sum of paid times) - (number of free walls so far),
        # r clamped to at most n (extra slack beyond n is never needed).
        # r ranges in [-n, n].
        dp = [INF] * (2 * n + 1)
        dp[n] = 0
        for i in range(n):
            new = [INF] * (2 * n + 1)
            c, t = cost[i], time[i]
            for idx in range(2 * n + 1):
                cur = dp[idx]
                if cur == INF:
                    continue
                r = idx - n
                # Paid painter paints wall i
                nr = min(n, r + t)
                if cur + c < new[nr + n]:
                    new[nr + n] = cur + c
                # Free painter paints wall i (needs r >= 1 for a paid painter to be busy)
                if r - 1 >= -n and cur < new[r - 1 + n]:
                    new[r - 1 + n] = cur
            dp = new
        return min(dp[n:])
