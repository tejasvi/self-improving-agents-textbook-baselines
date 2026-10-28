from math import gcd
from typing import List


class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        # dp[a][b]: number of ways (over processed elements) to form
        # disjoint seq1 with gcd a and seq2 with gcd b (0 = empty).
        dp = {(0, 0): 1}
        for x in nums:
            new = dict(dp)  # element x not used
            for (a, b), v in dp.items():
                na = gcd(a, x)
                key = (na, b)
                new[key] = (new.get(key, 0) + v) % MOD
                nb = gcd(b, x)
                key = (a, nb)
                new[key] = (new.get(key, 0) + v) % MOD
            dp = new
        ans = 0
        for (a, b), v in dp.items():
            if a == b and a > 0:
                ans = (ans + v) % MOD
        return ans
