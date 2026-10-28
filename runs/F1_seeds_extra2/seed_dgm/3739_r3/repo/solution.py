class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        N = m * n

        # Sum of pairwise Manhattan distances over all ordered-by-row/col cell pairs,
        # each unordered pair of cells counted once.
        total = 0
        for dx in range(1, m):
            total += dx * (m - dx) * n * n
        for dy in range(1, n):
            total += dy * (n - dy) * m * m
        total %= MOD

        # Number of arrangements containing a given pair of cells: C(N-2, k-2)
        r = k - 2
        a = N - 2
        # C(a, r) mod p via modular inverse
        num = 1
        den = 1
        for i in range(r):
            num = num * (a - i) % MOD
            den = den * (i + 1) % MOD
        comb = num * pow(den, MOD - 2, MOD) % MOD

        return total * comb % MOD
