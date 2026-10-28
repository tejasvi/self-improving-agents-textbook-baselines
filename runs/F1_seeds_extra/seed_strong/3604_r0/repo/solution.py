from typing import *


class Solution:
    def numberOfWays(self, n: int, x: int, y: int) -> int:
        MOD = 10**9 + 7
        # S[k] = Stirling number of second kind S(i, k), rolled over i
        S = [0] * (n + 1)
        S[0] = 1
        for i in range(1, n + 1):
            for k in range(i, 0, -1):
                S[k] = (S[k - 1] + k * S[k]) % MOD
            S[0] = 0
        ans = 0
        perm = 1  # x!/(x-k)!
        ypow = 1
        for k in range(1, min(n, x) + 1):
            perm = perm * (x - k + 1) % MOD
            ypow = ypow * y % MOD
            ans = (ans + S[k] * perm % MOD * ypow) % MOD
        return ans
