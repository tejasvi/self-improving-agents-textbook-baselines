from typing import List
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full = (1 << m) - 1
        INF = float("inf")

        # lcm for every nonempty subset of targets
        lcm_of = [1] * (1 << m)
        for mask in range(1, 1 << m):
            low = mask & -mask
            i = low.bit_length() - 1
            prev = lcm_of[mask ^ low]
            lcm_of[mask] = prev * target[i] // gcd(prev, target[i])

        dp = [INF] * (1 << m)
        dp[0] = 0
        for x in nums:
            # cost of raising x to the nearest multiple of lcm for each subset
            costs = [(-x) % lcm_of[s] for s in range(1 << m)]
            new = dp[:]
            for mask in range(1 << m):
                cur = dp[mask]
                if cur == INF:
                    continue
                for s in range(1, 1 << m):
                    nm = mask | s
                    v = cur + costs[s]
                    if v < new[nm]:
                        new[nm] = v
            dp = new
        return int(dp[full])
