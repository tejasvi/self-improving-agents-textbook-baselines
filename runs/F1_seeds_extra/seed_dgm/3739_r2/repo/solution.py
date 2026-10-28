class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        total_cells = m * n

        # Sum of Manhattan distances over all unordered pairs of cells.
        # Row component: n^2 * sum_{d=1}^{m-1} d*(m-d) = n^2 * (m-1)m(m+1)/6
        # Column component: m^2 * sum_{d=1}^{n-1} d*(n-d) = m^2 * (n-1)n(n+1)/6
        pair_sum = (n * n * (m - 1) * m * (m + 1) // 6
                    + m * m * (n - 1) * n * (n + 1) // 6)

        # Number of arrangements containing a given pair of cells: C(mn-2, k-2)
        r = k - 2
        N = total_cells - 2
        if r < 0 or r > N:
            return 0
        # Compute C(N, r) mod p via multiplicative formula with modular inverse.
        num = 1
        den = 1
        for i in range(r):
            num = num * (N - i) % MOD
            den = den * (i + 1) % MOD
        comb = num * pow(den, MOD - 2, MOD) % MOD

        return comb * (pair_sum % MOD) % MOD
