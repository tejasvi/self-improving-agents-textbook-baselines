from typing import *

MOD = 10**9 + 7


class Solution:
    def numberOfWays(self, n: int, x: int, y: int) -> int:
        # S[i][k]: Stirling numbers of the second kind (partitions of i performers into k non-empty bands)
        prev = [1] + [0] * n  # row for i = 0
        for i in range(1, n + 1):
            cur = [0] * (n + 1)
            for k in range(1, i + 1):
                cur[k] = (k * prev[k] + prev[k - 1]) % MOD
            prev = cur
        S = prev  # row n

        ans = 0
        falling = 1  # x * (x-1) * ... * (x-k+1)
        ypow = 1
        for k in range(1, min(n, x) + 1):
            falling = falling * (x - k + 1) % MOD
            ypow = ypow * y % MOD
            ans = (ans + S[k] * falling % MOD * ypow) % MOD
        return ans
