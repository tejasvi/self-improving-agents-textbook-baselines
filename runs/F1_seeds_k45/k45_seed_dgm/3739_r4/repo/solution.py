class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # Precompute factorials and inverse factorials
        total_cells = m * n
        fact = [1] * (total_cells + 1)
        for i in range(1, total_cells + 1):
            fact[i] = fact[i-1] * i % MOD
        
        # Compute modular inverse using Fermat's little theorem
        def mod_inverse(a, mod):
            return pow(a, mod - 2, mod)
        
        # Binomial coefficient C(n, k) mod MOD
        def comb(n, k):
            if k < 0 or k > n:
                return 0
            return fact[n] * mod_inverse(fact[k], MOD) % MOD * mod_inverse(fact[n-k], MOD) % MOD
        
        # Number of ways to place k pieces with 2 specific cells occupied
        ways = comb(total_cells - 2, k - 2)
        
        result = 0
        
        # Calculate contribution from row differences
        for row1 in range(m):
            for row2 in range(row1 + 1, m):
                distance = row2 - row1
                # Each cell in row1 can be paired with each cell in row2
                pairs = n * n
                contribution = (pairs * distance % MOD) * ways % MOD
                result = (result + contribution) % MOD
        
        # Calculate contribution from column differences
        for col1 in range(n):
            for col2 in range(col1 + 1, n):
                distance = col2 - col1
                # Each cell in col1 can be paired with each cell in col2
                pairs = m * m
                contribution = (pairs * distance % MOD) * ways % MOD
                result = (result + contribution) % MOD
        
        return result
