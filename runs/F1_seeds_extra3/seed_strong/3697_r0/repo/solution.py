from typing import *
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        k = len(target)
        full = (1 << k) - 1
        # lcm for every nonempty subset of targets
        lcm = [1] * (full + 1)
        for m in range(1, full + 1):
            low = m & (-m)
            i = low.bit_length() - 1
            rest = m ^ low
            l = lcm[rest] if rest else 1
            t = target[i]
            lcm[m] = l * t // gcd(l, t)
        # submask lists for each mask (nonempty submasks)
        subs = [[] for _ in range(full + 1)]
        for m in range(1, full + 1):
            s = m
            while s:
                subs[m].append(s)
                s = (s - 1) & m
        INF = float('inf')
        # Dedupe values: at most k copies of any value are ever useful
        cnt = {}
        for v in nums:
            c = cnt.get(v, 0)
            if c < k:
                cnt[v] = c + 1
        dp = [INF] * (full + 1)
        dp[0] = 0
        for v, c in cnt.items():
            for _ in range(c):
                # cost to cover subset s with v
                cost = [0] * (full + 1)
                for s in range(1, full + 1):
                    L = lcm[s]
                    cost[s] = (-(-v // L)) * L - v
                nd = dp[:]
                for m in range(1, full + 1):
                    best = nd[m]
                    for s in subs[m]:
                        val = dp[m ^ s] + cost[s]
                        if val < best:
                            best = val
                    nd[m] = best
                dp = nd
        return int(dp[full])
