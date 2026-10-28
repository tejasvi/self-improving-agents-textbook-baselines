from typing import *
import heapq
import math


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        k = len(target)
        full = (1 << k) - 1

        # lcm for each nonempty subset of targets
        lcm = [1] * (full + 1)
        for mask in range(1, full + 1):
            low = mask & -mask
            i = low.bit_length() - 1
            lcm[mask] = math.lcm(lcm[mask ^ low], target[i])

        # Each subset S needs one num; an optimal solution uses at most k nums,
        # so for each subset only the k cheapest candidates matter.
        cand = set()
        for S in range(1, full + 1):
            L = lcm[S]
            best = heapq.nsmallest(
                k, range(len(nums)), key=lambda j: (-nums[j]) % L
            )
            cand.update(best)

        INF = float("inf")
        dp = [INF] * (full + 1)
        dp[0] = 0
        for j in cand:
            x = nums[j]
            cost = [0] * (full + 1)
            for S in range(1, full + 1):
                cost[S] = (-x) % lcm[S]
            new = dp[:]
            for mask in range(full + 1):
                if dp[mask] == INF:
                    continue
                comp = full ^ mask
                S = comp
                while S:
                    v = dp[mask] + cost[S]
                    if v < new[mask | S]:
                        new[mask | S] = v
                    S = (S - 1) & comp
            dp = new
        return int(dp[full])
