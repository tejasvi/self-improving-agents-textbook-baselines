from typing import List
from math import gcd


class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        # dp[(a, b)]: number of ways to assign processed elements to seq1 (gcd a),
        # seq2 (gcd b), or neither. 0 denotes an empty sequence.
        dp = {(0, 0): 1}
        for x in nums:
            new = dict(dp)  # element unused
            for (a, b), c in dp.items():
                key = (gcd(a, x), b)
                new[key] = (new.get(key, 0) + c) % MOD
                key = (a, gcd(b, x))
                new[key] = (new.get(key, 0) + c) % MOD
            dp = new
        ans = 0
        for (a, b), c in dp.items():
            if a == b and a > 0:
                ans = (ans + c) % MOD
        return ans
