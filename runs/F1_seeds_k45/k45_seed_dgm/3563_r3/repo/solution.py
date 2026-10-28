from typing import List

class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        """
        Select cells from grid with maximum score.
        Constraints:
        - No two selected cells from same row
        - All selected values must be unique
        
        Approach: DFS with memoization
        State: (current_row, used_values_as_frozenset)
        """
        memo = {}
        
        def dfs(row: int, used_values: frozenset) -> int:
            # Base case: processed all rows
            if row == len(grid):
                return 0
            
            # Create a hashable key for memoization
            key = (row, used_values)
            if key in memo:
                return memo[key]
            
            # Option 1: Skip this row (don't select any cell from this row)
            max_score = dfs(row + 1, used_values)
            
            # Option 2: Select one cell from this row
            for col in range(len(grid[row])):
                value = grid[row][col]
                # Only select if value hasn't been used before
                if value not in used_values:
                    new_used = used_values | {value}
                    score = value + dfs(row + 1, new_used)
                    max_score = max(max_score, score)
            
            memo[key] = max_score
            return max_score
        
        result = dfs(0, frozenset())
        # The problem states "one or more cells", but the result should be at least 0
        # However, we can always select at least one cell, so result will be > 0
        return result
