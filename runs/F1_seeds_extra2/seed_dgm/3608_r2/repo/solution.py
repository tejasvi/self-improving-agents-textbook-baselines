from typing import List
from math import gcd


class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        # dp[(a, b)] = number of ways to split processed elements into
        # seq1 (gcd a, 0 = empty) and seq2 (gcd b, 0 = empty), rest unused.
        dp = {(0, 0): 1}
        for x in nums:
            new = dict(dp)  # element unused
            for (a, b), v in dp.items():
                k = (gcd(a, x), b)
                new[k] = (new.get(k, 0) + v) % MOD
                k = (a, gcd(b, x))
                new[k] = (new.get(k, 0) + v) % MOD
            dp = new
        ans = 0
        for (a, b), v in dp.items():
            if a == b and a > 0:
                ans = (ans + v) % MOD
        return ans
