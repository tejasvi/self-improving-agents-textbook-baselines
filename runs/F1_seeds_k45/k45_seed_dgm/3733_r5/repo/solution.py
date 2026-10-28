from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        """
        Find the length of the longest V-shaped diagonal segment.
        
        A V-shaped diagonal segment:
        - Starts with 1
        - Follows sequence: 2, 0, 2, 0, ...
        - Starts in one of 4 diagonal directions
        - Can make at most one 90-degree clockwise turn
        """
        if not grid or not grid[0]:
            return 0
        
        n, m = len(grid), len(grid[0])
        max_length = 0
        
        # Define 4 diagonal directions: (row_delta, col_delta)
        # 0: top-left to bottom-right (dr=1, dc=1)
        # 1: top-right to bottom-left (dr=1, dc=-1)
        # 2: bottom-right to top-left (dr=-1, dc=-1)
        # 3: bottom-left to top-right (dr=-1, dc=1)
        directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        
        # Clockwise turns for each direction
        # If moving in direction i, clockwise turn leads to direction (i+1)%4
        clockwise = {
            0: 1,  # (1,1) -> (1,-1)
            1: 2,  # (1,-1) -> (-1,-1)
            2: 3,  # (-1,-1) -> (-1,1)
            3: 0   # (-1,1) -> (1,1)
        }
        
        # Try each cell as a starting point
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 1:
                    # Try each direction
                    for dir_idx in range(4):
                        length = self.dfs(grid, i, j, dir_idx, 0, directions, clockwise)
                        max_length = max(max_length, length)
        
        return max_length
    
    def dfs(self, grid, row, col, direction, sequence_idx, directions, clockwise):
        """
        DFS to find length of V-shaped segment starting from (row, col).
        
        sequence_idx: 0 for 1, 1 for 2, 2 for 0, 3 for 2, 4 for 0, ...
        """
        n, m = len(grid), len(grid[0])
        
        # Check bounds
        if row < 0 or row >= n or col < 0 or col >= m:
            return 0
        
        # Expected value at current position
        if sequence_idx == 0:
            expected = 1
        else:
            # Pattern is 2, 0, 2, 0, ...
            expected = 2 if (sequence_idx - 1) % 2 == 0 else 0
        
        # Check if current cell matches expected value
        if grid[row][col] != expected:
            return 0
        
        # Base case: current cell is valid
        current_length = 1
        
        # Try to continue in the same direction
        dr, dc = directions[direction]
        next_row, next_col = row + dr, col + dc
        
        if 0 <= next_row < n and 0 <= next_col < m:
            continuation = self.dfs(grid, next_row, next_col, direction, sequence_idx + 1, directions, clockwise)
            current_length += continuation
            
            # If we continued, return (don't try turn)
            if continuation > 0:
                return current_length
        
        # Try to turn clockwise (only once per path)
        # We can only turn if sequence_idx > 1 (we've seen at least one 2 or 0)
        if sequence_idx > 0:  # Can only turn after we've moved at least once
            new_dir = clockwise[direction]
            dr_new, dc_new = directions[new_dir]
            next_row_turn, next_col_turn = row + dr_new, col + dc_new
            
            if 0 <= next_row_turn < n and 0 <= next_col_turn < m:
                turn_continuation = self.dfs(grid, next_row_turn, next_col_turn, new_dir, sequence_idx + 1, directions, clockwise)
                if turn_continuation > 0:
                    current_length += turn_continuation
        
        return current_length
