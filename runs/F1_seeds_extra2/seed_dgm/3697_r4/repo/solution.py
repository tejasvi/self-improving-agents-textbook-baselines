from math import gcd
from typing import List


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full = (1 << m) - 1
        INF = float("inf")

        # LCM of each subset of targets
        lcm_of = [1] * (1 << m)
        for s in range(1, 1 << m):
            low = s & -s
            i = low.bit_length() - 1
            prev = lcm_of[s ^ low]
            lcm_of[s] = prev * target[i] // gcd(prev, target[i])

        dp = [INF] * (1 << m)
        dp[0] = 0
        for x in nums:
            cost = [0] * (1 << m)
            for s in range(1, 1 << m):
                L = lcm_of[s]
                cost[s] = (L - x % L) % L
            new = dp[:]
            for mask in range(full + 1):
                base = dp[mask]
                if base == INF:
                    continue
                comp = full ^ mask
                sub = comp
                while sub:
                    nm = mask | sub
                    v = base + cost[sub]
                    if v < new[nm]:
                        new[nm] = v
                    sub = (sub - 1) & comp
            dp = new
        return int(dp[full])
