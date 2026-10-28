from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        """
        Find the length of the longest V-shaped diagonal segment.
        
        The segment:
        - Starts with value 1
        - Follows the sequence: 2, 0, 2, 0, ...
        - Moves diagonally in one direction
        - Can make at most one clockwise 90-degree turn
        """
        n = len(grid)
        m = len(grid[0])
        max_length = 0
        
        # Four diagonal directions: (row_delta, col_delta)
        # 0: down-right (↓→)
        # 1: down-left (↓←)
        # 2: up-left (↑←)
        # 3: up-right (↑→)
        directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        
        # Clockwise turn mapping: from direction i to direction (i + 1) % 4
        # down-right → down-left
        # down-left → up-left
        # up-left → up-right
        # up-right → down-right
        
        # For each cell that contains 1, try starting from there
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 1:
                    # Try each of the 4 directions
                    for dir_idx in range(4):
                        length = self._findLongestPath(grid, i, j, dir_idx, -1, 1)
                        max_length = max(max_length, length)
        
        return max_length
    
    def _findLongestPath(self, grid: List[List[int]], row: int, col: int, 
                        dir_idx: int, turn_used: int, seq_value: int) -> int:
        """
        Find the longest path starting from (row, col) in direction dir_idx.
        
        Args:
            grid: The grid
            row, col: Current position
            dir_idx: Current direction index (0-3)
            turn_used: -1 if turn not used, dir_idx if turn used in direction turn_used
            seq_value: Next expected value in sequence (1 initially, then alternates 2, 0)
        
        Returns:
            Length of the longest valid path from this position
        """
        n = len(grid)
        m = len(grid[0])
        directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        
        # Current position is already valid, length is 1 (starting with 1)
        # Now we need to continue the sequence
        max_length = 1
        
        # Try to continue in the same direction
        dr, dc = directions[dir_idx]
        next_row, next_col = row + dr, col + dc
        
        if 0 <= next_row < n and 0 <= next_col < m and grid[next_row][next_col] == 2:
            # Continue with sequence 2, 0, 2, 0, ...
            length = 1 + self._continue_path(grid, next_row, next_col, dir_idx, turn_used, 0)
            max_length = max(max_length, length)
        
        # Try a clockwise turn if not used yet
        if turn_used == -1:
            new_dir_idx = (dir_idx + 1) % 4
            dr, dc = directions[new_dir_idx]
            next_row, next_col = row + dr, col + dc
            
            if 0 <= next_row < n and 0 <= next_col < m and grid[next_row][next_col] == 2:
                # Make the turn and continue
                length = 1 + self._continue_path(grid, next_row, next_col, new_dir_idx, new_dir_idx, 0)
                max_length = max(max_length, length)
        
        return max_length
    
    def _continue_path(self, grid: List[List[int]], row: int, col: int,
                       dir_idx: int, turn_used: int, seq_index: int) -> int:
        """
        Continue the path from a position that we know has the correct value.
        
        Args:
            grid: The grid
            row, col: Current position (already validated)
            dir_idx: Current direction
            turn_used: -1 if turn not used, dir_idx if turn used
            seq_index: Position in the sequence [2, 0, 2, 0, ...] (0 means next is 2, 1 means next is 0)
        
        Returns:
            Length of the path starting from the next position
        """
        n = len(grid)
        m = len(grid[0])
        directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        
        # Current position count is 1 (already counted in caller)
        length = 1
        
        sequence = [2, 0]  # Repeating pattern
        
        # Try to continue in the same direction
        dr, dc = directions[dir_idx]
        next_row, next_col = row + dr, col + dc
        expected_value = sequence[seq_index % 2]
        
        if 0 <= next_row < n and 0 <= next_col < m and grid[next_row][next_col] == expected_value:
            # Continue in same direction
            length += self._continue_path(grid, next_row, next_col, dir_idx, turn_used, 
                                         (seq_index + 1) % 2)
        elif turn_used == -1:
            # Try a clockwise turn
            new_dir_idx = (dir_idx + 1) % 4
            dr, dc = directions[new_dir_idx]
            next_row, next_col = row + dr, col + dc
            
            if 0 <= next_row < n and 0 <= next_col < m and grid[next_row][next_col] == expected_value:
                # Make the turn and continue
                length += self._continue_path(grid, next_row, next_col, new_dir_idx, new_dir_idx,
                                             (seq_index + 1) % 2)
        
        return length
