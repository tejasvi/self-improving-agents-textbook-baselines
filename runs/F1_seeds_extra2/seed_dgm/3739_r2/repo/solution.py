class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10 ** 9 + 7
        N = m * n

        # Sum over unordered cell pairs of Manhattan distance.
        row_sum = sum(d * (m - d) for d in range(1, m)) * n * n
        col_sum = sum(d * (n - d) for d in range(1, n)) * m * m
        total = (row_sum + col_sum) % MOD

        # Number of arrangements containing a fixed pair: C(N-2, k-2).
        r = N - 2
        s = k - 2
        comb = 1
        if 0 <= s <= r:
            # Compute C(r, s) mod p via factorials.
            num = 1
            den = 1
            for i in range(s):
                num = num * (r - i) % MOD
                den = den * (i + 1) % MOD
            comb = num * pow(den, MOD - 2, MOD) % MOD
        else:
            comb = 0

        return total * comb % MOD
