from typing import *
from math import comb

MOD = 10**9 + 7

class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        N = m * n
        # sum over unordered cell pairs of |dr| = n^2 * (m^3 - m) / 6
        # sum over unordered cell pairs of |dc| = m^2 * (n^3 - n) / 6
        total = (n * n * ((m**3 - m) // 6) + m * m * ((n**3 - n) // 6)) % MOD
        return total * (comb(N - 2, k - 2) % MOD) % MOD
