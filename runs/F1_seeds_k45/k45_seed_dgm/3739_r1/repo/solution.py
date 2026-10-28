class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # Total cells
        total_cells = m * n
        
        # Calculate modular inverse using Fermat's little theorem
        def mod_inverse(a, mod):
            return pow(a, mod - 2, mod)
        
        # Step 1: Calculate sum of Manhattan distances for all pairs of cells
        # Manhattan distance = |x1 - x2| + |y1 - y2|
        # We can separate this into x-distance and y-distance
        
        # Sum of |x1 - x2| for all pairs of cells
        # For each pair of rows (x1, x2) with x1 < x2:
        # Contribution = |x2 - x1| * n * n (n cells in each row)
        x_distance_sum = 0
        for x1 in range(m):
            for x2 in range(x1 + 1, m):
                x_distance_sum += (x2 - x1) * n * n
        
        # Sum of |y1 - y2| for all pairs of cells
        # For each pair of columns (y1, y2) with y1 < y2:
        # Contribution = |y2 - y1| * m * m (m cells in each column)
        y_distance_sum = 0
        for y1 in range(n):
            for y2 in range(y1 + 1, n):
                y_distance_sum += (y2 - y1) * m * m
        
        # Total sum of Manhattan distances for all pairs of cells
        total_distance_sum = x_distance_sum + y_distance_sum
        
        # Step 2: Each pair of cells appears in C(total_cells - 2, k - 2) arrangements
        # The factor is: C(total_cells - 2, k - 2) / C(total_cells, k)
        #             = (k * (k - 1)) / (total_cells * (total_cells - 1))
        
        # However, we need to multiply total_distance_sum by the number of arrangements
        # where a specific pair of cells has pieces
        # Total arrangements = C(total_cells, k)
        # Arrangements with pieces at specific 2 cells = C(total_cells - 2, k - 2)
        
        # The contribution is:
        # sum_over_all_cell_pairs(distance * C(total_cells - 2, k - 2))
        # = C(total_cells - 2, k - 2) * total_distance_sum
        
        # But we need this modulo MOD
        # C(total_cells - 2, k - 2) = (total_cells - 2)! / ((k - 2)! * (total_cells - k)!)
        
        # We can use the formula:
        # C(n, r) = n! / (r! * (n-r)!)
        # C(total_cells, k) = total_cells! / (k! * (total_cells - k)!)
        
        # Let's use a different approach:
        # C(total_cells - 2, k - 2) = C(total_cells, k) * k * (k - 1) / (total_cells * (total_cells - 1))
        
        # So the answer is:
        # total_distance_sum * k * (k - 1) / (total_cells * (total_cells - 1)) (mod MOD)
        
        # But since we're working with modular arithmetic, we need to be careful
        # Answer = (total_distance_sum * k * (k - 1) * inv(total_cells * (total_cells - 1))) mod MOD
        
        numerator = (total_distance_sum % MOD) * (k % MOD) % MOD
        numerator = numerator * ((k - 1) % MOD) % MOD
        
        denominator = (total_cells % MOD) * ((total_cells - 1) % MOD) % MOD
        
        inv_denominator = mod_inverse(denominator, MOD)
        
        result = (numerator * inv_denominator) % MOD
        
        return result
