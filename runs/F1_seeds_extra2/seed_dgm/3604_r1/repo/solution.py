class Solution:
    def numberOfWays(self, n: int, x: int, y: int) -> int:
        MOD = 10**9 + 7
        # Stirling numbers of the second kind S(n, k), rolling over rows
        # S(i, k) = k * S(i-1, k) + S(i-1, k-1)
        m = min(n, x)
        S = [1] + [0] * m  # row i = 0
        for i in range(1, n + 1):
            new = [0] * (m + 1)
            for k in range(1, min(i, m) + 1):
                new[k] = (k * S[k] + S[k - 1]) % MOD
            S = new
        # S now holds row n
        total = 0
        perm = 1  # x! / (x-k)!  for k = 0
        ypow = 1  # y^k
        for k in range(1, m + 1):
            perm = perm * (x - k + 1) % MOD
            ypow = ypow * y % MOD
            total = (total + S[k] * perm % MOD * ypow) % MOD
        return total
