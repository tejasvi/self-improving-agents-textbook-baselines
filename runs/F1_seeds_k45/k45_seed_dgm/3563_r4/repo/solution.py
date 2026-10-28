class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        """
        Select cells from grid such that:
        1. No two cells from same row
        2. All selected values are unique
        
        Returns maximum sum of selected values.
        """
        memo = {}
        
        def dfs(row, used_values):
            """
            row: current row index
            used_values: frozenset of values already used
            returns: maximum score from this row onwards
            """
            # Base case: no more rows
            if row == len(grid):
                return 0
            
            # Create state key for memoization
            state = (row, used_values)
            if state in memo:
                return memo[state]
            
            # Option 1: Skip this row
            result = dfs(row + 1, used_values)
            
            # Option 2: Select one cell from current row
            for cell_value in grid[row]:
                # Only select if this value hasn't been used
                if cell_value not in used_values:
                    new_used = used_values | frozenset([cell_value])
                    result = max(result, cell_value + dfs(row + 1, new_used))
            
            memo[state] = result
            return result
        
        return dfs(0, frozenset())
