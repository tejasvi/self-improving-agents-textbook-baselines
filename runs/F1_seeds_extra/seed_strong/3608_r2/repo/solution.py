from typing import *
from math import gcd


class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        # state (g1, g2): gcd of seq1 and seq2 (0 = empty), value = number of ways
        dp = {(0, 0): 1}
        for x in nums:
            new = dict(dp)  # skip x
            for (a, b), c in dp.items():
                ka = (gcd(a, x), b)
                new[ka] = (new.get(ka, 0) + c) % MOD
                kb = (a, gcd(b, x))
                new[kb] = (new.get(kb, 0) + c) % MOD
            dp = new
        ans = 0
        for (a, b), c in dp.items():
            if a == b and a != 0:
                ans += c
        return ans % MOD
