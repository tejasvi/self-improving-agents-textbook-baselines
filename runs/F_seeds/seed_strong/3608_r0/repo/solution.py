from typing import *
from math import gcd

MOD = 10**9 + 7

class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        M = max(nums)
        # G[a][x] = gcd(a, x) for a in 0..M, x in 1..M
        G = [[gcd(a, x) for x in range(M + 1)] for a in range(M + 1)]
        # dp: dict keyed by (g1, g2) -> count, 0 means empty sequence
        dp = {(0, 0): 1}
        for x in nums:
            new = dict(dp)
            Gx = [G[a][x] for a in range(M + 1)]
            for (g1, g2), c in dp.items():
                k = (Gx[g1], g2)
                new[k] = (new.get(k, 0) + c) % MOD
                k = (g1, Gx[g2])
                new[k] = (new.get(k, 0) + c) % MOD
            dp = new
        ans = 0
        for (g1, g2), c in dp.items():
            if g1 == g2 and g1 > 0:
                ans = (ans + c) % MOD
        return ans
