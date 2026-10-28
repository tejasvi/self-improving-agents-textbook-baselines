from typing import List

class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        """
        Select cells from the grid such that:
        1. No two selected cells are in the same row
        2. All selected values are unique
        3. Maximize the sum of selected values
        
        Approach: Dynamic Programming with memoization
        - State: current row index and set of values already used
        - For each row, we can either:
          a. Skip the row entirely
          b. Select one cell from the row (if its value hasn't been used yet)
        """
        rows = len(grid)
        memo = {}
        
        def dp(row_idx, used_values):
            """
            Returns the maximum score starting from row_idx with used_values already selected.
            
            used_values: frozenset of values already used in previous rows
            """
            if row_idx == rows:
                return 0
            
            # Convert to frozenset for hashing
            key = (row_idx, used_values)
            if key in memo:
                return memo[key]
            
            # Option 1: Skip this row entirely
            result = dp(row_idx + 1, used_values)
            
            # Option 2: Select one cell from this row
            for cell_value in grid[row_idx]:
                if cell_value not in used_values:
                    # Select this cell
                    new_used = used_values | frozenset([cell_value])
                    result = max(result, cell_value + dp(row_idx + 1, new_used))
            
            memo[key] = result
            return result
        
        # Start with empty set of used values
        return dp(0, frozenset())
