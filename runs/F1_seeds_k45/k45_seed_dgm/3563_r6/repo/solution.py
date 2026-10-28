from typing import List

class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        """
        Select cells from grid to maximize score with constraints:
        1. No two cells from same row
        2. All selected values must be unique
        
        Approach: Dynamic programming with memoization
        - Process rows one by one
        - Track used values to ensure uniqueness
        - For each row, try selecting each value that hasn't been used
        """
        memo = {}
        
        def dp(row: int, used_values: frozenset) -> int:
            """
            Returns the maximum score starting from 'row' with 'used_values' already selected.
            
            Args:
                row: Current row index
                used_values: Frozenset of values already selected from previous rows
                
            Returns:
                Maximum score achievable from this state onwards
            """
            # Base case: processed all rows
            if row == len(grid):
                return 0
            
            # Check memoization
            key = (row, used_values)
            if key in memo:
                return memo[key]
            
            # Option 1: Skip this row
            result = dp(row + 1, used_values)
            
            # Option 2: Select a cell from this row
            # For maximum score, we should select values in descending order from current row
            # and only select if the value hasn't been used
            for value in grid[row]:
                if value not in used_values:
                    # Select this value and continue to next row
                    new_used = frozenset(used_values | {value})
                    result = max(result, value + dp(row + 1, new_used))
            
            memo[key] = result
            return result
        
        return dp(0, frozenset())
