class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # Precompute factorials and inverse factorials for combinations
        total_cells = m * n
        fact = [1] * (total_cells + 1)
        for i in range(1, total_cells + 1):
            fact[i] = fact[i-1] * i % MOD
        
        # Function to calculate modular inverse using Fermat's little theorem
        def mod_inverse(a, mod):
            return pow(a, mod - 2, mod)
        
        # Function to calculate C(n, k) mod MOD
        def comb(n, k):
            if k > n or k < 0:
                return 0
            if k == 0 or k == n:
                return 1
            return fact[n] * mod_inverse(fact[k], MOD) % MOD * mod_inverse(fact[n-k], MOD) % MOD
        
        # Number of ways to place k pieces such that two specific cells are occupied
        ways = comb(total_cells - 2, k - 2)
        
        # Calculate contribution from row differences
        row_contribution = 0
        for row1 in range(m):
            for row2 in range(row1 + 1, m):
                # Distance between these rows
                distance = row2 - row1
                # Number of cells in row1 is n, number of cells in row2 is n
                # Total pairs: n * n
                pairs_count = n * n % MOD
                row_contribution = (row_contribution + distance * pairs_count % MOD) % MOD
        
        # Calculate contribution from column differences
        col_contribution = 0
        for col1 in range(n):
            for col2 in range(col1 + 1, n):
                # Distance between these columns
                distance = col2 - col1
                # Number of cells in col1 is m, number of cells in col2 is m
                # Total pairs: m * m
                pairs_count = m * m % MOD
                col_contribution = (col_contribution + distance * pairs_count % MOD) % MOD
        
        # Total contribution = (row_contribution + col_contribution) * ways
        total = (row_contribution + col_contribution) % MOD
        total = total * ways % MOD
        
        return total
