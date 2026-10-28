class Solution:
    MOD = 10**9 + 7
    INV6 = pow(6, MOD-2, MOD)

    def distanceSum(self, m: int, n: int, k: int) -> int:
        # Number of cells
        N = m * n
        # Precompute factorials up to N for binomial coefficient C(N-2, k-2)
        # Since N <= 1e5, this is fast.
        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i-1] * i % self.MOD
        inv_fact = [1] * (N + 1)
        inv_fact[N] = pow(fact[N], self.MOD - 2, self.MOD)
        for i in range(N, 0, -1):
            inv_fact[i-1] = inv_fact[i] * i % self.MOD
        def comb(a, b):
            if b < 0 or b > a:
                return 0
            return fact[a] * inv_fact[b] % self.MOD * inv_fact[a-b] % self.MOD
        # Combination for choosing the remaining k-2 pieces after fixing a pair of cells
        ways = comb(N-2, k-2)
        # Compute sum over row distances for all unordered pairs of cells
        # S_row = sum_{d=1}^{m-1} d * (m - d) = (m-1)*m*(m+1)/6
        S_row = ( (m-1) * m % self.MOD) * (m+1) % self.MOD
        S_row = S_row * self.INV6 % self.MOD
        # Compute sum over column distances similarly
        S_col = ( (n-1) * n % self.MOD) * (n+1) % self.MOD
        S_col = S_col * self.INV6 % self.MOD
        # Contribution from row differences: each pair of rows contributes n^2 cells per row-pair
        term_row = pow(n, 2, self.MOD) * S_row % self.MOD
        # Contribution from column differences: each pair of columns contributes m^2 cells per column-pair
        term_col = pow(m, 2, self.MOD) * S_col % self.MOD
        total = (term_row + term_col) % self.MOD
        ans = ways * total % self.MOD
        return ans
