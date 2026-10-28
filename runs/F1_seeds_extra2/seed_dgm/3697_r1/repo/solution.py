from math import gcd
from typing import List


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full = (1 << m) - 1
        # lcm for each non-empty subset of targets
        lcm = [1] * (full + 1)
        for mask in range(1, full + 1):
            low = mask & -mask
            i = low.bit_length() - 1
            prev = lcm[mask ^ low]
            lcm[mask] = prev * target[i] // gcd(prev, target[i])
        subsets = list(range(1, full + 1))
        INF = float("inf")
        dp = [INF] * (full + 1)
        dp[0] = 0
        for x in nums:
            # cost of raising x to a multiple of lcm[S], for each subset S
            cost = {}
            for s in subsets:
                L = lcm[s]
                cost[s] = (L - x % L) % L
            new = dp[:]
            for mask in range(full + 1):
                d = dp[mask]
                if d == INF:
                    continue
                for s in subsets:
                    nm = mask | s
                    c = d + cost[s]
                    if c < new[nm]:
                        new[nm] = c
            dp = new
        return int(dp[full])
