from typing import *

MOD = 10**9 + 7


class Solution:
    def numberOfWays(self, n: int, x: int, y: int) -> int:
        # S[i][k]: Stirling numbers of the second kind (rolling rows)
        prev = [1]  # S(0,0) = 1
        for i in range(1, n + 1):
            cur = [0] * (i + 1)
            for k in range(1, i + 1):
                left = prev[k - 1] if k - 1 < len(prev) else 0
                right = prev[k] if k < len(prev) else 0
                cur[k] = (left + k * right) % MOD
            prev = cur
        # prev[k] = S(n, k)
        ans = 0
        perm = 1  # x!/(x-k)! accumulated
        ypow = 1
        for k in range(1, min(n, x) + 1):
            perm = perm * (x - k + 1) % MOD
            ypow = ypow * y % MOD
            ans = (ans + prev[k] * perm % MOD * ypow) % MOD
        return ans
