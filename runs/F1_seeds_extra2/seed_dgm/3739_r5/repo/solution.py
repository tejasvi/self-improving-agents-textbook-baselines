class Solution:
    MOD = 10**9 + 7

    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = self.MOD

        def pair_sum(L: int) -> int:
            # sum over ordered pairs (a, b) in [0, L) of |a - b|, divided by 2 (unordered)
            # = sum_{d=1}^{L-1} d * (L - d)
            return sum(d * (L - d) for d in range(1, L))

        N = m * n
        # Unordered cell pairs: row contribution n^2 * S_m, column contribution m^2 * S_n,
        # where S_L = sum over ordered row pairs of |diff|. Each unordered cell-pair sum
        # is half the ordered sum.
        total = (n * n * 2 * pair_sum(m) + m * m * 2 * pair_sum(n)) // 2
        total %= MOD

        # Number of arrangements containing a given unordered pair: C(N-2, k-2)
        r = N - 2
        t = k - 2
        # modular binomial
        num = 1
        for i in range(t):
            num = num * (r - i) % MOD
        den = 1
        for i in range(1, t + 1):
            den = den * i % MOD
        comb = num * pow(den, MOD - 2, MOD) % MOD

        return total * comb % MOD
