class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7

        def f(x: int) -> int:
            # sum over i < j in [0, x) of (j - i)
            return (x - 1) * x * (x + 1) // 6

        N = m * n
        total = (f(m) * n * n + f(n) * m * m) % MOD

        # C(N-2, k-2) modulo MOD
        r = k - 2
        num = 1
        den = 1
        for i in range(r):
            num = num * ((N - 2 - i) % MOD) % MOD
            den = den * ((i + 1) % MOD) % MOD
        comb = num * pow(den, MOD - 2, MOD) % MOD

        return total * comb % MOD
