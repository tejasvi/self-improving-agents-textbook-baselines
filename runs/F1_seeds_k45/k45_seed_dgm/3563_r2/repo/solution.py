from typing import List

class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        """
        Select cells from a matrix such that:
        - No two selected cells are in the same row
        - All selected cell values are unique
        - Return the maximum sum of selected values
        """
        num_rows = len(grid)
        memo = {}
        
        def dp(row: int, used_values: frozenset) -> int:
            """
            row: current row we're processing
            used_values: frozenset of values already selected from previous rows
            returns: maximum score from this row onwards
            """
            if row == num_rows:
                return 0
            
            key = (row, used_values)
            if key in memo:
                return memo[key]
            
            # Option 1: Skip this row (select nothing from this row)
            max_score = dp(row + 1, used_values)
            
            # Option 2: Select a cell from this row (if its value hasn't been used)
            for cell_value in grid[row]:
                if cell_value not in used_values:
                    # Add this value to used_values and move to next row
                    new_used = used_values | {cell_value}
                    score = cell_value + dp(row + 1, new_used)
                    max_score = max(max_score, score)
            
            memo[key] = max_score
            return max_score
        
        return dp(0, frozenset())
