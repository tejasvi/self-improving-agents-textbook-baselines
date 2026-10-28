from typing import List
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full = (1 << m) - 1
        INF = float("inf")

        # lcm of each non-empty subset of targets
        lcm = [1] * (full + 1)
        for mask in range(1, full + 1):
            low = mask & -mask
            i = low.bit_length() - 1
            rest = mask ^ low
            base = lcm[rest]
            lcm[mask] = base * target[i] // gcd(base, target[i])
        subsets = list(range(1, full + 1))

        dp = [INF] * (full + 1)
        dp[0] = 0
        for n in nums:
            # cost for n to become a multiple of lcm[sub]
            cost = {}
            for sub in subsets:
                L = lcm[sub]
                cost[sub] = (L - n % L) % L
            new = dp[:]
            for mask in range(full + 1):
                d = dp[mask]
                if d == INF:
                    continue
                for sub in subsets:
                    nm = mask | sub
                    v = d + cost[sub]
                    if v < new[nm]:
                        new[nm] = v
            dp = new
        return int(dp[full])
