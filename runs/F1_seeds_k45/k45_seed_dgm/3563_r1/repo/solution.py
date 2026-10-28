from typing import List

class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        """
        Select cells from grid such that:
        1. No two cells from same row
        2. All selected values are unique
        
        Maximize the sum of selected values.
        """
        num_rows = len(grid)
        
        # dp[used_values] = maximum score when using this set of values
        # used_values is a frozenset of values we've already selected
        dp = {frozenset(): 0}
        
        # Process each row
        for row in grid:
            new_dp = {}
            
            # For each state in current DP
            for used_values, score in dp.items():
                # Option 1: Don't select from this row
                if used_values not in new_dp:
                    new_dp[used_values] = score
                else:
                    new_dp[used_values] = max(new_dp[used_values], score)
                
                # Option 2: Select one cell from this row
                # Try each cell in the row
                for cell_value in row:
                    # Only select if value hasn't been used
                    if cell_value not in used_values:
                        new_used = frozenset(used_values | {cell_value})
                        new_score = score + cell_value
                        
                        if new_used not in new_dp:
                            new_dp[new_used] = new_score
                        else:
                            new_dp[new_used] = max(new_dp[new_used], new_score)
            
            dp = new_dp
        
        # Return the maximum score among all possible states
        return max(dp.values())
