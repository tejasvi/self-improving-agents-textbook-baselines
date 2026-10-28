class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        """
        Calculate the sum of Manhattan distances between every pair of pieces 
        over all valid arrangements.
        
        Key insight:
        - For each pair of cells, count how many arrangements have pieces at both cells
        - Number of such arrangements = C(m*n - 2, k - 2)
        - Manhattan distance = |x1 - x2| + |y1 - y2|
        
        We can decompose this into row and column contributions separately.
        For each pair of rows (or columns) at distance d, and each way to pick
        2 cells (one from each row/column), multiply by:
        - The distance d
        - C(m*n - 2, k - 2) (number of arrangements with pieces in both cells)
        
        Formula optimization:
        - For row contributions: sum over all pairs of rows with different distances
        - For column contributions: similarly
        """
        MOD = 10**9 + 7
        
        # Precompute factorials and inverse factorials for combinations
        total_cells = m * n
        
        # Precompute factorials
        fact = [1] * (total_cells + 1)
        for i in range(1, total_cells + 1):
            fact[i] = (fact[i-1] * i) % MOD
        
        # Compute modular inverse using Fermat's little theorem
        def modinv(a, mod):
            return pow(a, mod - 2, mod)
        
        # Compute combination C(n, r) mod MOD
        def comb(n, r):
            if r > n or r < 0:
                return 0
            return (fact[n] * modinv(fact[r], MOD) % MOD * modinv(fact[n-r], MOD)) % MOD
        
        # Number of ways to place k pieces such that 2 specific cells both have pieces
        arrangements_with_pair = comb(total_cells - 2, k - 2)
        
        result = 0
        
        # Contribution from row differences
        # For each pair of rows i1, i2 and each pair of columns j1, j2:
        # The row distance |i1 - i2| contributes to the total
        # Number of such arrangements = arrangements_with_pair
        # Sum over all pairs of rows: for each distance d, count pairs of rows with distance d
        
        # For each distance d from 1 to m-1:
        # Number of pairs of rows with distance d = m - d
        # Number of ways to pick 2 cells from different rows with distance d:
        #   - Pick row i1 and i2 with distance d: (m - d) ways
        #   - Pick column j1 and j2: n * n ways (any columns)
        # Contribution = d * (m - d) * n * n * arrangements_with_pair
        
        for d in range(1, m):
            row_pairs = (m - d) * n * n % MOD
            contribution = d * row_pairs % MOD
            contribution = contribution * arrangements_with_pair % MOD
            result = (result + contribution) % MOD
        
        # Contribution from column differences
        # Similar logic but for columns
        for d in range(1, n):
            col_pairs = (n - d) * m * m % MOD
            contribution = d * col_pairs % MOD
            contribution = contribution * arrangements_with_pair % MOD
            result = (result + contribution) % MOD
        
        return result
