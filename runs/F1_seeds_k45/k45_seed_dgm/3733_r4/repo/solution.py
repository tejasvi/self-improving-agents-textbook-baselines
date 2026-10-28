from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        """
        Find the length of the longest V-shaped diagonal segment in the grid.
        
        A V-shaped diagonal segment:
        - Starts with 1
        - Followed by sequence: 2, 0, 2, 0, ...
        - Goes in a diagonal direction
        - Can make at most one 90-degree clockwise turn
        """
        n = len(grid)
        m = len(grid[0]) if n > 0 else 0
        
        max_length = 0
        
        # 4 diagonal directions: down-right, down-left, up-left, up-right
        # Direction order: 0=down-right, 1=down-left, 2=up-left, 3=up-right
        directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        
        # Clockwise 90-degree turn mapping
        # down-right (0) -> down-left (1) -> up-left (2) -> up-right (3) -> down-right (0)
        clockwise_turn = {0: 1, 1: 2, 2: 3, 3: 0}
        
        # Try starting from every cell that has value 1
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 1:
                    # Try all 4 directions as the initial direction
                    for initial_dir in range(4):
                        length = self._explore_v_shape(grid, i, j, initial_dir, directions, clockwise_turn)
                        max_length = max(max_length, length)
        
        return max_length
    
    def _explore_v_shape(self, grid, start_row, start_col, initial_dir, directions, clockwise_turn):
        """
        Explore a V-shaped path starting from (start_row, start_col) in the initial_dir.
        Returns the length of the valid V-shaped segment found.
        """
        n = len(grid)
        m = len(grid[0])
        
        # First, follow the initial direction as far as possible with the sequence 2, 0, 2, 0, ...
        length = 1  # Start with 1
        row, col = start_row, start_col
        dr, dc = directions[initial_dir]
        expected_value = 2  # After 1, we expect 2
        
        # Phase 1: Follow the initial direction
        while True:
            next_row, next_col = row + dr, col + dc
            
            # Check bounds
            if next_row < 0 or next_row >= n or next_col < 0 or next_col >= m:
                break
            
            # Check if the value matches the expected sequence
            if grid[next_row][next_col] != expected_value:
                break
            
            length += 1
            row, col = next_row, next_col
            expected_value = 2 if expected_value == 0 else 0
        
        # Phase 2: Try making a clockwise 90-degree turn at the current position
        turned_dir = clockwise_turn[initial_dir]
        dr_turned, dc_turned = directions[turned_dir]
        
        # Continue from the current position in the turned direction
        while True:
            next_row, next_col = row + dr_turned, col + dc_turned
            
            # Check bounds
            if next_row < 0 or next_row >= n or next_col < 0 or next_col >= m:
                break
            
            # Check if the value matches the expected sequence
            if grid[next_row][next_col] != expected_value:
                break
            
            length += 1
            row, col = next_row, next_col
            expected_value = 2 if expected_value == 0 else 0
        
        return length
