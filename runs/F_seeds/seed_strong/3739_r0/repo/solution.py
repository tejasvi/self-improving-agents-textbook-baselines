from typing import *


class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10 ** 9 + 7
        N = m * n
        # sum over unordered pairs of cells of Manhattan distance
        total = 0
        for d in range(1, m):
            total += d * (m - d) * n * n
        for d in range(1, n):
            total += d * (n - d) * m * m
        total %= MOD
        # each pair of cells is used in C(N-2, k-2) arrangements
        r = k - 2
        ways = 1
        if 0 <= r <= N - 2:
            num = 1
            den = 1
            for i in range(r):
                num = num * (N - 2 - i) % MOD
                den = den * (i + 1) % MOD
            ways = num * pow(den, MOD - 2, MOD) % MOD
        else:
            ways = 0
        return total * ways % MOD
