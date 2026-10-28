from typing import List
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        k = len(target)
        full = (1 << k) - 1
        # lcm for each nonempty subset of targets
        lcm = [1] * (full + 1)
        for m in range(1, full + 1):
            low = m & -m
            idx = low.bit_length() - 1
            rest = m ^ low
            v = lcm[rest] if rest else 1
            t = target[idx]
            lcm[m] = v * t // gcd(v, t)

        INF = float("inf")
        # For each subset, keep the 4 nums with smallest cost (at most 4 nums are used overall).
        candidates = set()
        for m in range(1, full + 1):
            L = lcm[m]
            best = sorted(range(len(nums)), key=lambda i: (L - nums[i] % L) % L)[:k]
            candidates.update(best)

        dp = [INF] * (full + 1)
        dp[0] = 0
        for i in candidates:
            x = nums[i]
            cost = [0] * (full + 1)
            for m in range(1, full + 1):
                L = lcm[m]
                cost[m] = (L - x % L) % L
            new = dp[:]
            for mask in range(full + 1):
                if dp[mask] == INF:
                    continue
                rem = full & ~mask
                # enumerate nonempty submasks of rem
                s = rem
                while s:
                    v = dp[mask] + cost[s]
                    if v < new[mask | s]:
                        new[mask | s] = v
                    s = (s - 1) & rem
            dp = new
        return int(dp[full])
