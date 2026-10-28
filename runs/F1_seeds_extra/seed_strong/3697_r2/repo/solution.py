from typing import *
import heapq
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        k = len(target)
        full = (1 << k) - 1

        # lcm of each nonempty subset of targets
        lcm = [1] * (full + 1)
        for mask in range(1, full + 1):
            low = mask & -mask
            i = low.bit_length() - 1
            rest = mask ^ low
            v = target[i]
            if rest:
                g = gcd(lcm[rest], v)
                v = lcm[rest] // g * v
            lcm[mask] = v

        def cost(n, L):
            return (-n) % L

        # For each subset, only the k cheapest numbers can matter
        # (an optimal solution uses at most k numbers).
        candidates = set()
        for mask in range(1, full + 1):
            L = lcm[mask]
            best = heapq.nsmallest(k, range(len(nums)), key=lambda j: cost(nums[j], L))
            for j in best:
                candidates.add(j)

        INF = float("inf")
        dp = [INF] * (full + 1)
        dp[0] = 0
        for j in candidates:
            n = nums[j]
            new = dp[:]
            for mask in range(full + 1):
                if dp[mask] == INF:
                    continue
                comp = full ^ mask
                sub = comp
                while sub:
                    c = dp[mask] + cost(n, lcm[sub])
                    if c < new[mask | sub]:
                        new[mask | sub] = c
                    sub = (sub - 1) & comp
            dp = new
        return int(dp[full])
