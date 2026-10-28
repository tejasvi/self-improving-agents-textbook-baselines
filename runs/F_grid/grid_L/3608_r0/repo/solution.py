from math import gcd
from typing import List


class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10 ** 9 + 7
        # dp[(g1, g2)] = number of ways to split processed elements into
        # seq1 (gcd g1), seq2 (gcd g2), or neither; 0 denotes an empty sequence.
        dp = {(0, 0): 1}
        for x in nums:
            ndp = dict(dp)  # element goes to neither sequence
            for (g1, g2), c in dp.items():
                k1 = (gcd(g1, x), g2)
                ndp[k1] = (ndp.get(k1, 0) + c) % MOD
                k2 = (g1, gcd(g2, x))
                ndp[k2] = (ndp.get(k2, 0) + c) % MOD
            dp = ndp
        ans = 0
        for (g1, g2), c in dp.items():
            if g1 == g2 and g1 > 0:
                ans = (ans + c) % MOD
        return ans
