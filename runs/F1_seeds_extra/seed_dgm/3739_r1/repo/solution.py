class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        # Sum of Manhattan distances over all unordered pairs of cells.
        total = 0
        for d in range(1, m):
            total += d * (m - d) * n * n
        for d in range(1, n):
            total += d * (n - d) * m * m
        total %= MOD
        # Each unordered cell pair appears together in C(mn-2, k-2) arrangements.
        N = m * n
        r = k - 2
        ways = 1
        # C(N-2, r) computed via multiplicative formula with modular inverse.
        num = 1
        den = 1
        for i in range(r):
            num = num * (N - 2 - i) % MOD
            den = den * (i + 1) % MOD
        ways = num * pow(den, MOD - 2, MOD) % MOD
        return total * ways % MOD
