from typing import *


class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        N = m * n

        def f(x: int) -> int:
            # sum of |i-j| over ordered pairs i,j in [0, x)
            return (x - 1) * x * (x + 1) // 3

        # sum over unordered cell pairs of Manhattan distance
        S = (n * n * f(m) + m * m * f(n)) // 2
        # C(N-2, k-2) via exact big integer arithmetic is too slow for 1e5 in
        # general, so use modular factorials.
        r = k - 2
        t = N - 2
        num = 1
        den = 1
        for i in range(r):
            num = num * (t - i) % MOD
            den = den * (i + 1) % MOD
        comb = num * pow(den, MOD - 2, MOD) % MOD
        return S % MOD * comb % MOD
