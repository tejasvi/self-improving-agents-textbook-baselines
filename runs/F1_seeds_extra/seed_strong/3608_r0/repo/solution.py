from typing import *
from math import gcd


class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10 ** 9 + 7
        M = max(nums)
        total = 0
        for g in range(1, M + 1):
            # only elements divisible by g can belong to seq1/seq2 with gcd g
            vals = [x for x in nums if x % g == 0]
            if len(vals) < 2:
                continue
            # state: (gcd1, gcd2) with 0 meaning empty; store gcd divided by g
            dp = {(0, 0): 1}
            for x in vals:
                y = x // g
                nd = dict(dp)  # skip x
                for (a, b), c in dp.items():
                    na = gcd(a, y)
                    key = (na, b)
                    nd[key] = (nd.get(key, 0) + c) % MOD
                    nb = gcd(b, y)
                    key = (a, nb)
                    nd[key] = (nd.get(key, 0) + c) % MOD
                dp = nd
            total += dp.get((1, 1), 0)
            total %= MOD
        return total % MOD
