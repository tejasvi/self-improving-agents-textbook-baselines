from typing import *
import heapq
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full = (1 << m) - 1
        INF = float('inf')

        # lcm of each non-empty subset of targets
        lcm_of = [1] * (1 << m)
        for S in range(1, 1 << m):
            low = S & -S
            j = low.bit_length() - 1
            prev = lcm_of[S ^ low]
            lcm_of[S] = prev * target[j] // gcd(prev, target[j])

        # Candidate indices: for each subset, the (m) cheapest numbers.
        # Optimal solution uses at most m numbers, so this suffices.
        cand = set()
        for S in range(1, 1 << m):
            L = lcm_of[S]
            idx = heapq.nsmallest(m, range(len(nums)),
                                  key=lambda i: (L - nums[i] % L) % L)
            cand.update(idx)

        dp = [INF] * (1 << m)
        dp[0] = 0
        for i in cand:
            x = nums[i]
            new = dp[:]
            costs = [0] * (1 << m)
            for S in range(1, 1 << m):
                L = lcm_of[S]
                costs[S] = (L - x % L) % L
            for mask in range(1 << m):
                if dp[mask] == INF:
                    continue
                base = dp[mask]
                for S in range(1, 1 << m):
                    nm = mask | S
                    v = base + costs[S]
                    if v < new[nm]:
                        new[nm] = v
            dp = new
        return int(dp[full])
