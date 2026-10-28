from typing import *


class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        N = m * n
        # Sum of |i-j| over all pairs of rows, times n^2 (column pairs)
        row = sum(d * (m - d) for d in range(1, m)) * n * n
        # Sum of |i-j| over all pairs of columns, times m^2 (row pairs)
        col = sum(d * (n - d) for d in range(1, n)) * m * m
        total = (row + col) % MOD
        # Number of arrangements containing a given pair of cells: C(N-2, k-2)
        r = k - 2
        t = N - 2
        num = 1
        den = 1
        for i in range(r):
            num = num * (t - i) % MOD
            den = den * (i + 1) % MOD
        comb = num * pow(den, MOD - 2, MOD) % MOD
        return total * comb % MOD
