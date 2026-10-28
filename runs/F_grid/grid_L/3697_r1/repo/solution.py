from typing import List
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full = (1 << m) - 1
        INF = float("inf")

        # lcm of each subset of targets
        lcm = [1] * (1 << m)
        for mask in range(1, 1 << m):
            low = mask & -mask
            j = low.bit_length() - 1
            prev = lcm[mask ^ low]
            lcm[mask] = prev * target[j] // gcd(prev, target[j])

        dp = [INF] * (1 << m)
        dp[0] = 0
        for n in nums:
            # cost for this number to cover each non-empty subset
            cost = [0] * (1 << m)
            for s in range(1, 1 << m):
                L = lcm[s]
                cost[s] = (-(-n // L)) * L - n
            new = dp[:]
            for mask in range(full + 1):
                if dp[mask] == INF:
                    continue
                rem = full & ~mask
                # choose a non-empty subset s of remaining targets
                s = rem
                while s:
                    v = dp[mask] + cost[s]
                    if v < new[mask | s]:
                        new[mask | s] = v
                    s = (s - 1) & rem
            dp = new
        return int(dp[full])
