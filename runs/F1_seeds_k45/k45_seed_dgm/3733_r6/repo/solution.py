from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        max_length = 0
        
        # Four diagonal directions: (dr, dc)
        # 0: (1, 1) - top-left to bottom-right
        # 1: (1, -1) - top-right to bottom-left
        # 2: (-1, -1) - bottom-right to top-left
        # 3: (-1, 1) - bottom-left to top-right
        directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        
        # Clockwise turns from each direction
        # (1, 1) -> (1, -1), (1, -1) -> (-1, -1), (-1, -1) -> (-1, 1), (-1, 1) -> (1, 1)
        clockwise_turn = {
            0: 1,  # (1, 1) -> (1, -1)
            1: 2,  # (1, -1) -> (-1, -1)
            2: 3,  # (-1, -1) -> (-1, 1)
            3: 0   # (-1, 1) -> (1, 1)
        }
        
        # Try starting from each cell with value 1
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 1:
                    # Try each of the 4 directions as initial direction
                    for dir_idx in range(4):
                        length = self._find_v_length(grid, i, j, dir_idx, directions, clockwise_turn)
                        max_length = max(max_length, length)
        
        return max_length
    
    def _find_v_length(self, grid, start_i, start_j, initial_dir_idx, directions, clockwise_turn):
        n = len(grid)
        m = len(grid[0])
        
        # Phase 1: Move in the initial direction with sequence 2, 0, 2, 0, ...
        length = 1  # Start with 1
        i, j = start_i, start_j
        dr, dc = directions[initial_dir_idx]
        sequence_idx = 0  # 0 for 2, 1 for 0, 2 for 2, 3 for 0, ...
        expected_vals = [2, 0]
        
        # Phase 1: Continue in the same direction
        while True:
            ni, nj = i + dr, j + dc
            if ni < 0 or ni >= n or nj < 0 or nj >= m:
                break
            expected = expected_vals[sequence_idx % 2]
            if grid[ni][nj] != expected:
                break
            length += 1
            i, j = ni, nj
            sequence_idx += 1
        
        # Now try a clockwise turn (optional)
        # After turning, we continue the sequence
        current_dir_idx = initial_dir_idx
        turned = False
        
        # Try making one clockwise turn
        next_dir_idx = clockwise_turn[current_dir_idx]
        dr, dc = directions[next_dir_idx]
        
        while True:
            ni, nj = i + dr, j + dc
            if ni < 0 or ni >= n or nj < 0 or nj >= m:
                break
            expected = expected_vals[sequence_idx % 2]
            if grid[ni][nj] != expected:
                break
            length += 1
            i, j = ni, nj
            sequence_idx += 1
            turned = True
        
        return length
