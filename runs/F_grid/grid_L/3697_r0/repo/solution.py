from typing import List
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full = (1 << m) - 1
        INF = float("inf")

        # lcm of each non-empty subset of targets
        lcm_of = [1] * (1 << m)
        for mask in range(1, 1 << m):
            low = mask & -mask
            i = low.bit_length() - 1
            prev = lcm_of[mask ^ low]
            t = target[i]
            lcm_of[mask] = prev * t // gcd(prev, t)

        dp = [INF] * (1 << m)
        dp[0] = 0
        for n in nums:
            # cost for this num to become a multiple of lcm of each subset
            cost = [0] * (1 << m)
            for sub in range(1, 1 << m):
                L = lcm_of[sub]
                cost[sub] = (-n) % L
            new = dp[:]
            for mask in range(full + 1):
                base = dp[mask]
                if base == INF:
                    continue
                comp = full ^ mask
                sub = comp
                while sub:
                    val = base + cost[sub]
                    nm = mask | sub
                    if val < new[nm]:
                        new[nm] = val
                    sub = (sub - 1) & comp
            dp = new
        return int(dp[full])
