MOD = 10**9 + 7

class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        # Total cells
        N = m * n
        if k < 2:
            return 0
        # Precompute factorials up to N for combinations
        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i - 1] * i % MOD
        inv_fact = [1] * (N + 1)
        inv_fact[N] = pow(fact[N], MOD - 2, MOD)
        for i in range(N, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD
        def comb(nn, rr):
            if rr < 0 or rr > nn:
                return 0
            return fact[nn] * inv_fact[rr] % MOD * inv_fact[nn - rr] % MOD
        # Number of ways to pick the remaining k-2 pieces after fixing a pair
        ways = comb(N - 2, k - 2)
        # Sum of Manhattan distances over all unordered pairs of cells
        # Row contribution: n^2 * sum_{r1<r2} (r2 - r1)
        # Column contribution: m^2 * sum_{c1<c2} (c2 - c1)
        inv6 = pow(6, MOD - 2, MOD)
        row_diff_sum = (pow(m, 3, MOD) - m) % MOD  # = m*(m^2-1)
        col_diff_sum = (pow(n, 3, MOD) - n) % MOD  # = n*(n^2-1)
        row_part = pow(n, 2, MOD) * row_diff_sum % MOD
        col_part = pow(m, 2, MOD) * col_diff_sum % MOD
        total_pairs_sum = (row_part + col_part) % MOD
        total_pairs_sum = total_pairs_sum * inv6 % MOD
        return ways * total_pairs_sum % MOD
