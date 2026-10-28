from math import gcd
from typing import List


class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        # dp[(a, b)] = number of ways to assign processed elements to seq1 (gcd a),
        # seq2 (gcd b), or neither. gcd 0 denotes an empty sequence.
        dp = {(0, 0): 1}
        for x in nums:
            new = dict(dp)  # x goes to neither
            for (a, b), c in dp.items():
                ga = gcd(a, x)
                key = (ga, b)
                new[key] = (new.get(key, 0) + c) % MOD  # x goes to seq1
                gb = gcd(b, x)
                key = (a, gb)
                new[key] = (new.get(key, 0) + c) % MOD  # x goes to seq2
            dp = new
        return sum(c for (a, b), c in dp.items() if a == b and a > 0) % MOD
