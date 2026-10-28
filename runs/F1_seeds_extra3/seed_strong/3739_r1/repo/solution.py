from typing import *


class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        N = m * n
        # sum over all unordered cell pairs of Manhattan distance
        total = n * n * ((m**3 - m) // 6) + m * m * ((n**3 - n) // 6)
        # each unordered pair of cells is used in C(N-2, k-2) arrangements
        r = k - 2
        ways = 1
        for i in range(r):
            ways = ways * (N - 2 - i) % MOD
        fact = 1
        for i in range(1, r + 1):
            fact = fact * i % MOD
        ways = ways * pow(fact, MOD - 2, MOD) % MOD
        return total % MOD * ways % MOD
