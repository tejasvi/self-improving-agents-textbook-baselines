from typing import List

class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        """
        Select cells from grid with maximum score such that:
        1. No two cells are in the same row
        2. All selected values are unique
        
        We use dynamic programming where we process rows one by one.
        State: dp[row][used_values] = maximum score achievable with the given set of used values
        
        Using recursion with memoization.
        At each row, we can either:
        1. Skip this row entirely
        2. Select one cell from this row (if its value hasn't been used yet)
        """
        m = len(grid)  # number of rows
        n = len(grid[0])  # number of columns
        
        memo = {}
        
        def dfs(row, used_values):
            """
            row: current row we're processing
            used_values: frozenset of values we've already used
            returns: maximum score from this row onwards
            """
            if row == m:
                return 0
            
            if (row, used_values) in memo:
                return memo[(row, used_values)]
            
            # Option 1: Skip this row entirely
            max_score = dfs(row + 1, used_values)
            
            # Option 2: Select one cell from this row
            for col in range(n):
                cell_value = grid[row][col]
                
                # Can only select if this value hasn't been used
                if cell_value not in used_values:
                    new_used = used_values | frozenset([cell_value])
                    score = cell_value + dfs(row + 1, new_used)
                    max_score = max(max_score, score)
            
            memo[(row, used_values)] = max_score
            return max_score
        
        return dfs(0, frozenset())
