from typing import *


class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10 ** 9 + 7

        def F(L: int) -> int:
            # sum_{d=1}^{L-1} d*(L-d)
            return (L - 1) * L * (L + 1) // 6

        N = m * n
        total = (n * n * F(m) + m * m * F(n)) % MOD
        # C(N-2, k-2) mod p
        r = k - 2
        a = N - 2
        num = 1
        den = 1
        for i in range(r):
            num = num * (a - i) % MOD
            den = den * (i + 1) % MOD
        comb = num * pow(den, MOD - 2, MOD) % MOD
        return total * comb % MOD
