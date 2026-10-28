class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7

        def pair_sum(L: int) -> int:
            # sum over d of d * (L - d)
            return sum(d * (L - d) for d in range(1, L))

        N = m * n
        # Sum of Manhattan distances over all unordered pairs of cells
        S = (n * n * pair_sum(m) + m * m * pair_sum(n)) % MOD

        # C(N-2, k-2) mod p
        r = k - 2
        t = N - 2
        num = 1
        den = 1
        for i in range(r):
            num = num * (t - i) % MOD
            den = den * (i + 1) % MOD
        comb = num * pow(den, MOD - 2, MOD) % MOD

        return S * comb % MOD
