from math import gcd
from typing import List


class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        # dp[(g1, g2)] = number of ways to assign processed elements to
        # seq1 / seq2 / neither with gcd(seq1)=g1 and gcd(seq2)=g2.
        # gcd 0 represents an empty sequence.
        dp = {(0, 0): 1}
        for x in nums:
            new = dict(dp)  # element goes to neither
            for (a, b), c in dp.items():
                key = (gcd(a, x), b)
                new[key] = (new.get(key, 0) + c) % MOD
                key = (a, gcd(b, x))
                new[key] = (new.get(key, 0) + c) % MOD
            dp = new
        return sum(c for (a, b), c in dp.items() if a == b and a > 0) % MOD
