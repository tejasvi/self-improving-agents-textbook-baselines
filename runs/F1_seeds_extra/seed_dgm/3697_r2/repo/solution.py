from typing import List
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full = (1 << m) - 1
        INF = float("inf")

        # lcm for every non-empty subset of targets
        lcm_of = [1] * (1 << m)
        for s in range(1, 1 << m):
            low = s & -s
            i = low.bit_length() - 1
            prev = lcm_of[s ^ low]
            lcm_of[s] = prev * target[i] // gcd(prev, target[i])

        subsets = list(range(1, 1 << m))
        dp = [INF] * (1 << m)
        dp[0] = 0

        for x in nums:
            # Cost of raising x to a multiple of each subset's lcm
            cost = [0] * (1 << m)
            for s in subsets:
                L = lcm_of[s]
                cost[s] = (L - x % L) % L
            new_dp = dp[:]
            for mask in range(full + 1):
                cur = dp[mask]
                if cur == INF:
                    continue
                for s in subsets:
                    nm = mask | s
                    v = cur + cost[s]
                    if v < new_dp[nm]:
                        new_dp[nm] = v
            dp = new_dp

        return int(dp[full])
