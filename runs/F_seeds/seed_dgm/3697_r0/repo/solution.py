from math import gcd
from typing import List


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full = (1 << m) - 1
        INF = float("inf")

        # lcm of each non-empty subset of targets
        lcm_of = [1] * (1 << m)
        for s in range(1, 1 << m):
            low = s & -s
            i = low.bit_length() - 1
            rest = s ^ low
            l = lcm_of[rest] if rest else 1
            t = target[i]
            lcm_of[s] = l * t // gcd(l, t)

        # Subsets with their lcm, excluding empty set
        subsets = [s for s in range(1, 1 << m)]

        dp = [INF] * (1 << m)
        dp[0] = 0
        for n in nums:
            # cost of raising n to a multiple of lcm of subset s
            cost = {s: (-n) % lcm_of[s] for s in subsets}
            new = dp[:]
            for mask in range(1 << m):
                if dp[mask] == INF:
                    continue
                free = full ^ mask
                # enumerate non-empty submasks of free
                sub = free
                while sub:
                    val = dp[mask] + cost[sub]
                    if val < new[mask | sub]:
                        new[mask | sub] = val
                    sub = (sub - 1) & free
            dp = new
        return int(dp[full])
