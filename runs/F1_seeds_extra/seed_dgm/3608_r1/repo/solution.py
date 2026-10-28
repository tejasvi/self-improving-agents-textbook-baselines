from typing import List
from math import gcd


class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        # dp[(g1, g2)] = number of ways to split processed elements into
        # seq1 (gcd g1), seq2 (gcd g2), or unused; 0 denotes an empty sequence.
        dp = {(0, 0): 1}
        for x in nums:
            new = dict(dp)  # element unused
            for (a, b), cnt in dp.items():
                na = gcd(a, x)
                key = (na, b)
                new[key] = (new.get(key, 0) + cnt) % MOD
                nb = gcd(b, x)
                key = (a, nb)
                new[key] = (new.get(key, 0) + cnt) % MOD
            dp = new
        ans = 0
        for (a, b), cnt in dp.items():
            if a and a == b:
                ans = (ans + cnt) % MOD
        return ans
