class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10 ** 9 + 7
        N = m * n

        # Number of arrangements containing a specific pair of cells: C(N-2, k-2)
        def comb(a, b):
            if b < 0 or b > a:
                return 0
            num = 1
            den = 1
            for i in range(b):
                num = num * (a - i) % MOD
                den = den * (i + 1) % MOD
            return num * pow(den, MOD - 2, MOD) % MOD

        total = 0
        for d in range(1, m):
            total += d * (m - d) % MOD * (n * n % MOD)
        for d in range(1, n):
            total += d * (n - d) % MOD * (m * m % MOD)
        total %= MOD

        return total * comb(N - 2, k - 2) % MOD
