class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # Precompute factorials and inverse factorials for combinations
        total_cells = m * n
        
        # Helper function to compute combination C(n, k)
        def comb(n, k):
            if k > n or k < 0:
                return 0
            if k == 0 or k == n:
                return 1
            
            # Use the formula: C(n,k) = n! / (k! * (n-k)!)
            numerator = 1
            denominator = 1
            for i in range(k):
                numerator = numerator * (n - i) % MOD
                denominator = denominator * (i + 1) % MOD
            
            # Compute modular inverse using Fermat's little theorem
            return numerator * pow(denominator, MOD - 2, MOD) % MOD
        
        # Number of arrangements where a specific pair of cells both have pieces
        pair_arrangements = comb(total_cells - 2, k - 2)
        
        # Calculate sum of Manhattan distances between all pairs of cells
        distance_sum = 0
        
        # Contribution from row differences
        # For each pair of rows (r1, r2) where r1 < r2, 
        # count how many cell pairs have these row indices
        for r1 in range(m):
            for r2 in range(r1 + 1, m):
                row_distance = r2 - r1
                # Number of cell pairs with rows r1 and r2
                pairs_with_these_rows = n * n
                distance_sum += row_distance * pairs_with_these_rows
        
        # Contribution from column differences
        # For each pair of columns (c1, c2) where c1 < c2,
        # count how many cell pairs have these column indices
        for c1 in range(n):
            for c2 in range(c1 + 1, n):
                col_distance = c2 - c1
                # Number of cell pairs with columns c1 and c2
                pairs_with_these_cols = m * m
                distance_sum += col_distance * pairs_with_these_cols
        
        # Result is pair_arrangements * distance_sum
        result = (pair_arrangements * distance_sum) % MOD
        return result
