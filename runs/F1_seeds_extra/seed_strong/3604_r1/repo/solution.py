from typing import *

MOD = 10**9 + 7


class Solution:
    def numberOfWays(self, n: int, x: int, y: int) -> int:
        # S[i][k]: Stirling numbers of the second kind (partitions of i performers into k non-empty bands)
        prev = [1]  # i = 0
        for i in range(1, n + 1):
            cur = [0] * (i + 1)
            for k in range(1, i + 1):
                left = prev[k - 1] if k - 1 < len(prev) else 0
                right = prev[k] if k < len(prev) else 0
                cur[k] = (k * right + left) % MOD
            prev = cur
        total = 0
        perm = 1  # x * (x-1) * ... * (x-k+1)
        ypow = 1
        for k in range(1, min(n, x) + 1):
            perm = perm * (x - k + 1) % MOD
            ypow = ypow * y % MOD
            total = (total + prev[k] * perm % MOD * ypow) % MOD
        return total
