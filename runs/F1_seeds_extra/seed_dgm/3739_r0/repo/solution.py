import math


class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10 ** 9 + 7
        N = m * n
        total = 0
        for dx in range(m):
            for dy in range(n):
                if dx == 0 and dy == 0:
                    continue
                mult = 2 if (dx > 0 and dy > 0) else 1
                total += mult * (dx + dy) * (m - dx) * (n - dy)
        ways = math.comb(N - 2, k - 2)
        return total % MOD * (ways % MOD) % MOD
