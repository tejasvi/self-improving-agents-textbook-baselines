class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10 ** 9 + 7
        N = m * n

        def pair_sum(L):
            # sum over d in [1, L-1] of d * (L - d)
            return sum(d * (L - d) for d in range(1, L)) % MOD

        # Sum of Manhattan distances over all unordered pairs of cells
        total = (n * n % MOD) * pair_sum(m) + (m * m % MOD) * pair_sum(n)
        total %= MOD

        # Number of ways to place the remaining k-2 pieces: C(N-2, k-2)
        def comb(a, b):
            if b < 0 or b > a:
                return 0
            num = 1
            den = 1
            for i in range(b):
                num = num * (a - i) % MOD
                den = den * (i + 1) % MOD
            return num * pow(den, MOD - 2, MOD) % MOD

        return total * comb(N - 2, k - 2) % MOD
