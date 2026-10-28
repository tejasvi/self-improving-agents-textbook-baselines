from math import gcd
from typing import List


class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        # dp[(g1, g2)] = number of ways to split processed elements into
        # seq1 (GCD g1), seq2 (GCD g2), and unused; 0 denotes empty.
        dp = {(0, 0): 1}
        for x in nums:
            new = {}
            for (a, b), c in dp.items():
                # skip x
                new[(a, b)] = (new.get((a, b), 0) + c) % MOD
                # add x to seq1
                k = (gcd(a, x), b)
                new[k] = (new.get(k, 0) + c) % MOD
                # add x to seq2
                k = (a, gcd(b, x))
                new[k] = (new.get(k, 0) + c) % MOD
            dp = new
        ans = 0
        for (a, b), c in dp.items():
            if a >= 1 and a == b:
                ans = (ans + c) % MOD
        return ans
