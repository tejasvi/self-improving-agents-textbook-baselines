from typing import List

class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        """
        Select cells from the grid such that:
        1. No two cells are in the same row
        2. All selected values are unique
        3. Maximize the sum of selected values
        """
        memo = {}
        
        def dfs(row_idx, used_values):
            # Base case: processed all rows
            if row_idx == len(grid):
                return 0
            
            # Convert used_values to a frozenset for hashing
            used_key = frozenset(used_values)
            
            # Check memo
            if (row_idx, used_key) in memo:
                return memo[(row_idx, used_key)]
            
            # Option 1: Skip this row
            result = dfs(row_idx + 1, used_values)
            
            # Option 2: Select a cell from this row
            for value in grid[row_idx]:
                # Only select if this value hasn't been used
                if value not in used_values:
                    new_used = used_values | {value}
                    result = max(result, value + dfs(row_idx + 1, new_used))
            
            memo[(row_idx, used_key)] = result
            return result
        
        return dfs(0, set())
