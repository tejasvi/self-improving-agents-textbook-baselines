class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        N = m * n

        def S(x: int) -> int:
            # sum over 0 <= i < j <= x-1 of (j - i)
            return (x - 1) * x * (x + 1) // 6

        # C(N-2, k-2) modulo MOD
        top, bot = N - 2, k - 2
        num = 1
        den = 1
        for i in range(bot):
            num = num * (top - i) % MOD
            den = den * (i + 1) % MOD
        comb = num * pow(den, MOD - 2, MOD) % MOD

        total = (n * n * S(m) + m * m * S(n)) % MOD
        return comb * total % MOD
