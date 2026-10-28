class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # Precompute factorials and inverse factorials for combinations
        max_val = m * n
        fact = [1] * (max_val + 1)
        for i in range(1, max_val + 1):
            fact[i] = fact[i-1] * i % MOD
        
        # Compute modular inverse using Fermat's little theorem
        def mod_inverse(a, mod):
            return pow(a, mod - 2, mod)
        
        # Function to compute C(n, k) mod MOD
        def comb(n, k):
            if k < 0 or k > n:
                return 0
            return fact[n] * mod_inverse(fact[k], MOD) % MOD * mod_inverse(fact[n-k], MOD) % MOD
        
        # Number of arrangements where both cells have pieces
        # We choose 2 cells fixed, then choose k-2 from remaining m*n-2 cells
        arrangements_with_pair = comb(m * n - 2, k - 2)
        
        # Calculate row contribution
        # For each pair of rows i1, i2: sum of |i1 - i2| * (number of cells in row i1) * (number of cells in row i2)
        row_contribution = 0
        for i1 in range(m):
            for i2 in range(i1 + 1, m):
                distance = i2 - i1
                # Each row has n cells
                contribution = distance * n * n % MOD
                row_contribution = (row_contribution + contribution) % MOD
        
        # Calculate column contribution
        # For each pair of columns j1, j2: sum of |j1 - j2| * (number of cells in col j1) * (number of cells in col j2)
        col_contribution = 0
        for j1 in range(n):
            for j2 in range(j1 + 1, n):
                distance = j2 - j1
                # Each column has m cells
                contribution = distance * m * m % MOD
                col_contribution = (col_contribution + contribution) % MOD
        
        # Total contribution = (row_contribution + col_contribution) * arrangements_with_pair
        result = (row_contribution + col_contribution) % MOD
        result = result * arrangements_with_pair % MOD
        
        return result
