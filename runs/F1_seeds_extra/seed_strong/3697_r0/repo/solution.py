from typing import *
import heapq
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full = (1 << m) - 1
        # lcm for each nonempty subset of targets
        lcm_of = [1] * (1 << m)
        for S in range(1, 1 << m):
            low = S & -S
            j = low.bit_length() - 1
            rest = S ^ low
            l = lcm_of[rest] if rest else 1
            t = target[j]
            lcm_of[S] = l * t // gcd(l, t)

        # Candidate pool: for each subset, the m cheapest elements (by cost
        # to become a multiple of lcm). An optimal solution can be assumed to
        # only use such candidates (exchange argument with at most m uses).
        cand = set()
        for S in range(1, 1 << m):
            L = lcm_of[S]
            best = heapq.nsmallest(
                m, range(len(nums)), key=lambda i: (-nums[i]) % L
            )
            cand.update(best)

        INF = float('inf')
        dp = [INF] * (1 << m)
        dp[0] = 0
        for i in cand:
            x = nums[i]
            new = dp[:]
            for mask in range(1 << m):
                if dp[mask] == INF:
                    continue
                for S in range(1, 1 << m):
                    c = dp[mask] + (-x) % lcm_of[S]
                    nm = mask | S
                    if c < new[nm]:
                        new[nm] = c
            dp = new
        return int(dp[full])
