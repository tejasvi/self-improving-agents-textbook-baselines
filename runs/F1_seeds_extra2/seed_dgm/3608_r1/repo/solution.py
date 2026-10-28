from math import gcd
from typing import List


class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        # dp[(g1, g2)] = number of ways to assign processed elements to
        # seq1 (gcd g1), seq2 (gcd g2), or neither; gcd 0 means empty.
        dp = {(0, 0): 1}
        for x in nums:
            new = dict(dp)  # element left out of both
            for (g1, g2), c in dp.items():
                k = (gcd(g1, x), g2)
                new[k] = (new.get(k, 0) + c) % MOD
                k = (g1, gcd(g2, x))
                new[k] = (new.get(k, 0) + c) % MOD
            dp = new
        return sum(c for (g1, g2), c in dp.items() if g1 == g2 and g1 > 0) % MOD
