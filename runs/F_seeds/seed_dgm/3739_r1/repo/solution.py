class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10 ** 9 + 7
        N = m * n

        def A(x: int) -> int:
            # sum over d in [1, x-1] of d * (x - d)
            return sum(d * (x - d) for d in range(1, x)) % MOD

        # sum over all unordered pairs of cells of Manhattan distance
        total_pairs = (n * n % MOD * A(m) + m * m % MOD * A(n)) % MOD

        # C(N-2, k-2) mod p
        r = k - 2
        num = 1
        den = 1
        for i in range(r):
            num = num * (N - 2 - i) % MOD
            den = den * (i + 1) % MOD
        comb = num * pow(den, MOD - 2, MOD) % MOD

        return total_pairs * comb % MOD
