class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7
        # choose which k adjacent pairs are equal: C(n-1, k)
        # first element: m choices; each of the remaining n-1-k "changed" pairs: (m-1) choices
        num = 1
        den = 1
        for i in range(k):
            num = num * (n - 1 - i) % MOD
            den = den * (i + 1) % MOD
        comb = num * pow(den, MOD - 2, MOD) % MOD
        return comb * m % MOD * pow(m - 1, n - 1 - k, MOD) % MOD
