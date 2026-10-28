MOD = 10**9 + 7

class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        """Return sum of Manhattan distances over all arrangements of k identical pieces.
        The total sum equals C(N-2, k-2) * S where N=m*n and S is the sum of distances over all unordered
        pairs of distinct cells.
        """
        N = m * n
        # Precompute factorials up to N
        fact = [1] * (N + 1)
        for i in range(2, N + 1):
            fact[i] = fact[i - 1] * i % MOD
        inv_fact = [1] * (N + 1)
        inv_fact[N] = pow(fact[N], MOD - 2, MOD)
        for i in range(N, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        def comb(a: int, b: int) -> int:
            if b < 0 or b > a:
                return 0
            return fact[a] * inv_fact[b] % MOD * inv_fact[a - b] % MOD

        # Number of ways to choose remaining k-2 pieces after fixing a pair of cells:
        ways = comb(N - 2, k - 2)

        # Compute S = sum_{unordered pairs} Manhattan distance
        # Separate row and column contributions.
        # Row contribution: for each pair of rows i<j, distance = (j-i) and there are n*n column choices.
        # Sum_{i<j} (j-i) = m*(m-1)*(m+1)//6
        row_pair_sum = m * (m - 1) * (m + 1) // 6
        col_pair_sum = n * (n - 1) * (n + 1) // 6
        S = (n * n % MOD) * (row_pair_sum % MOD) % MOD
        S = (S + (m * m % MOD) * (col_pair_sum % MOD)) % MOD
        # The formula derived already divides by 6, row_pair_sum and col_pair_sum include that division.

        ans = ways * S % MOD
        return ans
