from typing import *


class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10 ** 9 + 7
        N = m * n
        # sum over unordered cell pairs of |dr| = n^2 * sum_{d} d(m-d) = n^2 * (m^3 - m) / 6
        H = n * n * (m ** 3 - m) // 6
        V = m * m * (n ** 3 - n) // 6
        total = (H + V) % MOD
        # C(N-2, k-2) mod p
        r = k - 2
        t = N - 2
        comb = 1
        for i in range(r):
            comb = comb * (t - i) % MOD
        fact = 1
        for i in range(1, r + 1):
            fact = fact * i % MOD
        comb = comb * pow(fact, MOD - 2, MOD) % MOD
        return total * comb % MOD
