from typing import List
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full = (1 << m) - 1
        INF = float("inf")

        # lcm of each nonempty subset of targets
        lcm_of = [1] * (1 << m)
        for mask in range(1, 1 << m):
            low = mask & -mask
            i = low.bit_length() - 1
            prev = lcm_of[mask ^ low]
            lcm_of[mask] = prev * target[i] // gcd(prev, target[i])

        dp = [INF] * (1 << m)
        dp[0] = 0
        for a in nums:
            new = dp[:]  # this num covers nothing
            for S in range(1 << m):
                base = dp[S]
                if base == INF:
                    continue
                free = full ^ S
                c = free
                while c:
                    cost = base + (-a) % lcm_of[c]
                    if cost < new[S | c]:
                        new[S | c] = cost
                    c = (c - 1) & free
            dp = new
        return int(dp[full])
