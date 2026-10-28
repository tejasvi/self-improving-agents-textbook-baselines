from math import gcd
from typing import List


class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        # dp[g1][g2]: number of ways to assign processed elements to seq1 (gcd g1),
        # seq2 (gcd g2), or neither; 0 denotes an empty sequence.
        dp = {(0, 0): 1}
        for x in nums:
            new = dict(dp)  # element not used
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
