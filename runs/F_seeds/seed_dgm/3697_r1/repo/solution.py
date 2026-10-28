from typing import List
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full = (1 << m) - 1
        # lcm of each non-empty subset of targets
        lcm_of = [1] * (1 << m)
        for s in range(1, 1 << m):
            low = s & -s
            idx = low.bit_length() - 1
            prev = lcm_of[s ^ low]
            t = target[idx]
            lcm_of[s] = prev // gcd(prev, t) * t

        INF = float("inf")
        dp = [INF] * (1 << m)
        dp[0] = 0
        for x in nums:
            new = dp[:]
            for mask in range(1 << m):
                cur = dp[mask]
                if cur == INF:
                    continue
                rest = full ^ mask
                s = rest
                while s:
                    cost = cur + (-x) % lcm_of[s]
                    nm = mask | s
                    if cost < new[nm]:
                        new[nm] = cost
                    s = (s - 1) & rest
            dp = new
        return int(dp[full])
