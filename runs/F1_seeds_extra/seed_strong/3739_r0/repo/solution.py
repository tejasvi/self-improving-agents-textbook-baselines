from typing import *


class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        N = m * n
        # sum over unordered cell pairs of |dr| and |dc|
        row = n * n * sum(d * (m - d) for d in range(1, m))
        col = m * m * sum(d * (n - d) for d in range(1, n))
        total = (row + col) % MOD
        # C(N-2, k-2) mod p
        r = k - 2
        num = 1
        den = 1
        for i in range(r):
            num = num * (N - 2 - i) % MOD
            den = den * (i + 1) % MOD
        comb = num * pow(den, MOD - 2, MOD) % MOD
        return total * comb % MOD
