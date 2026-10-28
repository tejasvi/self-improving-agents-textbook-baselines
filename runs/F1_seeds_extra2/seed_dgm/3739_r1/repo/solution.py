class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10 ** 9 + 7
        N = m * n

        def S(x: int) -> int:
            # sum over d in [1, x-1] of d * (x - d)
            return sum(d * (x - d) for d in range(1, x)) % MOD

        # Sum over all unordered cell pairs of |dr| + |dc|
        total = (n * n % MOD * S(m) + m * m % MOD * S(n)) % MOD

        # Number of arrangements containing a given pair: C(N-2, k-2)
        r = k - 2
        t = N - 2
        num = 1
        den = 1
        for i in range(r):
            num = num * (t - i) % MOD
            den = den * (i + 1) % MOD
        comb = num * pow(den, MOD - 2, MOD) % MOD

        return total * comb % MOD
