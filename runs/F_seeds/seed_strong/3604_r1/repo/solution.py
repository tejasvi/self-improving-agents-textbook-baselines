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
                cur[k] = (left + k * right) % MOD
            prev = cur
        # falling factorial x*(x-1)*...*(x-k+1) and y^k
        total = 0
        falling = 1
        power = 1
        for k in range(1, min(n, x) + 1):
            falling = falling * (x - k + 1) % MOD
            power = power * y % MOD
            total = (total + prev[k] * falling % MOD * power) % MOD
        return total
