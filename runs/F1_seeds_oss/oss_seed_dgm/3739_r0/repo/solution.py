class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        mod = 10**9 + 7
        N = m * n
        # Precompute factorials up to N for combination calculations
        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i - 1] * i % mod
        inv_fact = [1] * (N + 1)
        inv_fact[N] = pow(fact[N], mod - 2, mod)
        for i in range(N, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % mod

        def comb(a, b):
            if b < 0 or b > a:
                return 0
            return fact[a] * inv_fact[b] % mod * inv_fact[a - b] % mod

        # Sum of Manhattan distances over all unordered pairs of cells
        inv6 = pow(6, mod - 2, mod)
        term1 = (n * n) % mod
        term1 = term1 * (m % mod) % mod
        term1 = term1 * ((m - 1) % mod) % mod
        term1 = term1 * ((m + 1) % mod) % mod

        term2 = (m * m) % mod
        term2 = term2 * (n % mod) % mod
        term2 = term2 * ((n - 1) % mod) % mod
        term2 = term2 * ((n + 1) % mod) % mod

        pair_sum = (term1 + term2) % mod
        pair_sum = pair_sum * inv6 % mod

        # Number of ways to choose remaining k-2 cells from the other N-2 cells
        ways = comb(N - 2, k - 2)
        return pair_sum * ways % mod
