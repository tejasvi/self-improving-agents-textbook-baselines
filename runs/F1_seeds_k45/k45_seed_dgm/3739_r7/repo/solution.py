class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # Precompute factorials and inverse factorials
        total_cells = m * n
        max_fact = total_cells + 1
        
        fact = [1] * max_fact
        for i in range(1, max_fact):
            fact[i] = fact[i-1] * i % MOD
        
        # Compute modular inverse using Fermat's little theorem
        def mod_inv(x):
            return pow(x, MOD - 2, MOD)
        
        inv_fact = [1] * max_fact
        inv_fact[-1] = mod_inv(fact[-1])
        for i in range(max_fact - 2, -1, -1):
            inv_fact[i] = inv_fact[i + 1] * (i + 1) % MOD
        
        # Compute C(n, k)
        def comb(n, k):
            if k < 0 or k > n:
                return 0
            return fact[n] * inv_fact[k] % MOD * inv_fact[n - k] % MOD
        
        # Number of arrangements where a specific pair of cells both have pieces
        pair_arrangements = comb(total_cells - 2, k - 2)
        
        # Calculate sum of distances in x dimension
        # For each pair of different x-coordinates (i, j) where i < j
        # There are n cells at x=i and n cells at x=j (i.e., n*n pairs)
        # Distance contribution: (j - i)
        x_distance_sum = 0
        for i in range(m):
            for j in range(i + 1, m):
                x_distance_sum = (x_distance_sum + (j - i)) % MOD
        
        # In x dimension: for each pair of x-coordinates, there are n^2 cell pairs
        x_contribution = x_distance_sum * (n * n) % MOD * pair_arrangements % MOD
        
        # Calculate sum of distances in y dimension
        # For each pair of different y-coordinates (i, j) where i < j
        y_distance_sum = 0
        for i in range(n):
            for j in range(i + 1, n):
                y_distance_sum = (y_distance_sum + (j - i)) % MOD
        
        # In y dimension: for each pair of y-coordinates, there are m^2 cell pairs
        y_contribution = y_distance_sum * (m * m) % MOD * pair_arrangements % MOD
        
        result = (x_contribution + y_contribution) % MOD
        return result
