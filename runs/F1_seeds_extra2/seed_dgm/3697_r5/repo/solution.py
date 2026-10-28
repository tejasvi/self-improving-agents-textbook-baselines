from math import gcd
from typing import List


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full = (1 << m) - 1
        INF = float("inf")

        # lcm of each non-empty subset of targets
        lcm_of = [1] * (1 << m)
        for mask in range(1, 1 << m):
            low = mask & -mask
            j = low.bit_length() - 1
            prev = lcm_of[mask ^ low]
            lcm_of[mask] = prev * target[j] // gcd(prev, target[j])

        dp = [INF] * (1 << m)
        dp[0] = 0
        for x in nums:
            # cost[S]: operations to raise x to a multiple of lcm(S)
            cost = [0] * (1 << m)
            for S in range(1, 1 << m):
                L = lcm_of[S]
                cost[S] = (L - x % L) % L
            new = dp[:]
            for mask in range(full + 1):
                if dp[mask] == INF:
                    continue
                rest = full ^ mask
                sub = rest
                while sub:
                    val = dp[mask] + cost[sub]
                    if val < new[mask | sub]:
                        new[mask | sub] = val
                    sub = (sub - 1) & rest
            dp = new
        return int(dp[full])
