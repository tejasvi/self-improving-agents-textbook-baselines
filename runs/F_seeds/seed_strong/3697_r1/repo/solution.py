from typing import *
from math import gcd
import heapq


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full = (1 << m) - 1
        INF = float('inf')

        # lcm for each nonempty subset of targets
        lcm = [1] * (1 << m)
        for s in range(1, 1 << m):
            low = s & -s
            i = low.bit_length() - 1
            prev = lcm[s ^ low]
            lcm[s] = prev * target[i] // gcd(prev, target[i])

        def cost(n: int, L: int) -> int:
            r = n % L
            return 0 if r == 0 else L - r

        # Only the m cheapest elements for each subset can matter (at most m
        # elements are ever used, and they are pairwise distinct).
        cand = set()
        for s in range(1, 1 << m):
            L = lcm[s]
            best = heapq.nsmallest(m, range(len(nums)),
                                   key=lambda idx: cost(nums[idx], L))
            for idx in best:
                cand.add(idx)

        dp = [INF] * (1 << m)
        dp[0] = 0
        for idx in cand:
            n = nums[idx]
            new = dp[:]
            costs = [0] * (1 << m)
            for s in range(1, 1 << m):
                costs[s] = cost(n, lcm[s])
            for mask in range(1 << m):
                if dp[mask] == INF:
                    continue
                comp = full ^ mask
                sub = comp
                while sub:
                    v = dp[mask] + costs[sub]
                    if v < new[mask | sub]:
                        new[mask | sub] = v
                    sub = (sub - 1) & comp
            dp = new
        return int(dp[full])
