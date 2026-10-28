from typing import List
import math

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full_mask = (1 << m) - 1
        # precompute lcm for each subset mask
        lcm_mask = [1] * (1 << m)
        for mask in range(1, 1 << m):
            # get lowest set bit
            l = 1
            for i in range(m):
                if mask & (1 << i):
                    l = l * target[i] // math.gcd(l, target[i])
            lcm_mask[mask] = l
        INF = 10**20
        dp = [INF] * (1 << m)
        dp[0] = 0
        # iterate over each number
        for num in nums:
            # compute cost to cover each subset using this number
            cost_for_mask = [0] * (1 << m)
            for mask in range(1, 1 << m):
                l = lcm_mask[mask]
                # smallest multiple of l >= num
                k = (num + l - 1) // l
                cost_for_mask[mask] = k * l - num
            # DP transition
            new_dp = dp[:]  # copy current dp
            for prev_mask in range(1 << m):
                if dp[prev_mask] == INF:
                    continue
                base = dp[prev_mask]
                for mask in range(1, 1 << m):
                    new_mask = prev_mask | mask
                    c = base + cost_for_mask[mask]
                    if c < new_dp[new_mask]:
                        new_dp[new_mask] = c
            dp = new_dp
        return dp[full_mask]
