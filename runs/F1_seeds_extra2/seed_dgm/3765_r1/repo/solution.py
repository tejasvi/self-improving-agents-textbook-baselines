from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # P[i]: prefix sum of nums, C[i]: prefix sum of cost (1-indexed, P[0]=C[0]=0)
        P = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            P[i + 1] = P[i] + nums[i]
            C[i + 1] = C[i] + cost[i]
        total = C[n]
        INF = float("inf")
        # dp[r]: minimum cost to split the first r elements
        dp = [0] + [INF] * n
        for r in range(1, n + 1):
            best = INF
            pr = P[r]
            cr = C[r]
            for l in range(1, r + 1):
                # segment nums[l-1..r-1] is the next subarray, starting at index l
                prev = dp[l - 1]
                cl = C[l - 1]
                val = prev + pr * (cr - cl) + k * (total - cl)
                if val < best:
                    best = val
            dp[r] = best
        return int(dp[n])
