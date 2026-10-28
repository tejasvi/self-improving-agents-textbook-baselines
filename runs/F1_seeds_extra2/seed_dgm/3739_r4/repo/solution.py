class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10 ** 9 + 7
        N = m * n

        # Sum over all unordered pairs of distinct cells of Manhattan distance.
        total = 0
        for d in range(1, m):
            total += d * (m - d) * n * n
        for d in range(1, n):
            total += d * (n - d) * m * m
        total %= MOD

        # Each unordered pair of cells is used in C(N-2, k-2) arrangements.
        a, b = N - 2, k - 2
        ways = 1
        for i in range(b):
            ways = ways * (a - i) % MOD
        fact_b = 1
        for i in range(1, b + 1):
            fact_b = fact_b * i % MOD
        ways = ways * pow(fact_b, MOD - 2, MOD) % MOD

        return total * ways % MOD
