from typing import *
from math import gcd
import heapq


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full = (1 << m) - 1

        # lcm for each nonempty subset of targets
        lcm_of = [1] * (1 << m)
        for s in range(1, 1 << m):
            low = s & -s
            j = low.bit_length() - 1
            rest = s ^ low
            t = target[j]
            base = lcm_of[rest] if rest else 1
            lcm_of[s] = base * t // gcd(base, t)

        # For each subset, keep the (m) nums with smallest cost; a group uses
        # one num, and at most m-1 other groups can block candidates.
        cand = set()
        for s in range(1, 1 << m):
            L = lcm_of[s]
            best = heapq.nsmallest(m, range(len(nums)), key=lambda i: (-nums[i]) % L)
            cand.update(best)

        INF = float('inf')
        dp = [INF] * (1 << m)
        dp[0] = 0
        for i in cand:
            x = nums[i]
            costs = [0] * (1 << m)
            for s in range(1, 1 << m):
                costs[s] = (-x) % lcm_of[s]
            new = dp[:]
            for mask in range(1 << m):
                if dp[mask] == INF:
                    continue
                dm = dp[mask]
                for s in range(1, 1 << m):
                    nm = mask | s
                    v = dm + costs[s]
                    if v < new[nm]:
                        new[nm] = v
            dp = new
        return int(dp[full])
