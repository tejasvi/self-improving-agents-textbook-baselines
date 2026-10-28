from typing import *
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full = (1 << m) - 1
        # lcm for each nonempty subset of targets
        lcms = [0] * (full + 1)
        for S in range(1, full + 1):
            l = 1
            for i in range(m):
                if S >> i & 1:
                    l = l * target[i] // gcd(l, target[i])
            lcms[S] = l
        subsets = list(range(1, full + 1))
        INF = float('inf')
        dp = [INF] * (full + 1)
        dp[0] = 0
        # each number at most once per target count; cap copies of equal values
        cnt = {}
        for x in nums:
            c = cnt.get(x, 0)
            if c >= m:
                continue
            cnt[x] = c + 1
            new = dp[:]
            for S in subsets:
                L = lcms[S]
                cost = (L - x % L) % L
                for mask in range(full + 1):
                    if dp[mask] == INF or mask & S:
                        continue
                    v = dp[mask] + cost
                    t = mask | S
                    if v < new[t]:
                        new[t] = v
            dp = new
        return int(dp[full])
