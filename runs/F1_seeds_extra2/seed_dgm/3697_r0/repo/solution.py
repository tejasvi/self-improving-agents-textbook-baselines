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

        # dp[mask] = min ops so that targets in mask are covered by processed nums
        dp = [INF] * (1 << m)
        dp[0] = 0
        subsets = list(range(1, 1 << m))

        for a in nums:
            # cost to raise a to the nearest multiple of lcm_of[sub] (>= a)
            cost = [0] * (1 << m)
            for sub in subsets:
                L = lcm_of[sub]
                cost[sub] = (L - a % L) % L
            new_dp = dp[:]  # element unused
            for mask in range(1 << m):
                cur = dp[mask]
                if cur == INF:
                    continue
                rest = full ^ mask
                # enumerate non-empty submasks of rest
                s = rest
                while s:
                    val = cur + cost[s]
                    nm = mask | s
                    if val < new_dp[nm]:
                        new_dp[nm] = val
                    s = (s - 1) & rest
            dp = new_dp

        return int(dp[full])
