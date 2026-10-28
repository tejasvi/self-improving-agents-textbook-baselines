class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        N = m * n
        # precompute factorials up to N
        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i-1] * i % MOD
        inv_fact = [1] * (N + 1)
        inv_fact[N] = pow(fact[N], MOD-2, MOD)
        for i in range(N, 0, -1):
            inv_fact[i-1] = inv_fact[i] * i % MOD
        # combination C(N-2, k-2)
        comb = fact[N-2] * inv_fact[k-2] % MOD * inv_fact[N - k] % MOD
        inv6 = pow(6, MOD-2, MOD)
        # sum of distances for row component
        # sum_{i<j} (j-i) = m*(m-1)*(m+1)/6
        row_part = (m * (m-1) % MOD) * (m+1) % MOD
        row_part = row_part * inv6 % MOD
        row_part = row_part * (n * n % MOD) % MOD
        # column component similar
        col_part = (n * (n-1) % MOD) * (n+1) % MOD
        col_part = col_part * inv6 % MOD
        col_part = col_part * (m * m % MOD) % MOD
        total = (row_part + col_part) % MOD
        ans = comb * total % MOD
        return ans
