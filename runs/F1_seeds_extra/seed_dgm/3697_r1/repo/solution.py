import heapq
from math import gcd
from typing import List


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full = (1 << m) - 1

        # lcm for every non-empty subset of targets
        lcm_of = [1] * (1 << m)
        for s in range(1, 1 << m):
            low = s & -s
            i = low.bit_length() - 1
            rest = s ^ low
            t = target[i]
            if rest == 0:
                lcm_of[s] = t
            else:
                prev = lcm_of[rest]
                lcm_of[s] = prev * t // gcd(prev, t)

        # Each subset is covered by one of the 4 cheapest nums for it
        # (exchange argument), so the candidate pool stays small.
        candidates = set()
        for s in range(1, 1 << m):
            L = lcm_of[s]
            best = heapq.nsmallest(
                m, range(len(nums)), key=lambda idx: (-nums[idx]) % L
            )
            candidates.update(best)

        INF = float("inf")
        dp = [INF] * (1 << m)
        dp[0] = 0
        for idx in candidates:
            x = nums[idx]
            new = dp[:]
            for mask in range(1 << m):
                if dp[mask] == INF:
                    continue
                for s in range(1, 1 << m):
                    cost = dp[mask] + (-x) % lcm_of[s]
                    nm = mask | s
                    if cost < new[nm]:
                        new[nm] = cost
            dp = new
        return int(dp[full])
