from math import gcd
from typing import List


class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        # dp[(g1, g2)] = number of ways to choose disjoint seq1/seq2 among
        # processed elements with gcd(seq1)=g1, gcd(seq2)=g2 (0 = empty).
        dp = {(0, 0): 1}
        for x in nums:
            new = dict(dp)  # x goes to neither
            for (g1, g2), c in dp.items():
                k1 = (gcd(g1, x), g2)
                new[k1] = (new.get(k1, 0) + c) % MOD
                k2 = (g1, gcd(g2, x))
                new[k2] = (new.get(k2, 0) + c) % MOD
            dp = new
        ans = 0
        for (g1, g2), c in dp.items():
            if g1 == g2 and g1 > 0:
                ans = (ans + c) % MOD
        return ans
