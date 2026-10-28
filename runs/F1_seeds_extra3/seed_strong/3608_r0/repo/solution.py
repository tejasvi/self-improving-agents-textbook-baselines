from typing import *
from math import gcd

MOD = 10**9 + 7

class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        M = 201
        # dp[a][b]: number of ways (assignments of processed elements) where
        # gcd of seq1 is a and gcd of seq2 is b; 0 denotes empty sequence.
        dp = {(0, 0): 1}
        for x in nums:
            new = dict(dp)  # x goes to neither
            for (a, b), v in dp.items():
                ga = gcd(a, x)
                k = (ga, b)
                new[k] = (new.get(k, 0) + v) % MOD
                gb = gcd(b, x)
                k = (a, gb)
                new[k] = (new.get(k, 0) + v) % MOD
            dp = new
        ans = 0
        for g in range(1, M):
            ans += dp.get((g, g), 0)
        return ans % MOD
