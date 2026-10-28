from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        """
        Find the length of the longest V-shaped diagonal segment in the grid.
        
        A V-shaped diagonal segment:
        - Starts with 1
        - Follows pattern: 2, 0, 2, 0, ...
        - Moves in one diagonal direction, then can make one 90-degree clockwise turn
        """
        if not grid or not grid[0]:
            return 0
        
        n, m = len(grid), len(grid[0])
        max_length = 0
        
        # Four diagonal directions: (dr, dc)
        # 0: down-right (1, 1)
        # 1: down-left (1, -1)
        # 2: up-left (-1, -1)
        # 3: up-right (-1, 1)
        directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        
        # For each possible starting position with value 1
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 1:
                    # Try each initial direction
                    for init_dir in range(4):
                        # Start with length 1 (the starting cell with value 1)
                        # Next expected value is 2 (index 0 in pattern)
                        memo = {}
                        length = self._search(grid, i, j, init_dir, directions, 0, 1, n, m, 
                                            has_turned=False, memo=memo)
                        max_length = max(max_length, length)
        
        return max_length
    
    def _search(self, grid, row, col, direction, directions, pattern_idx, length, n, m, 
                has_turned, memo):
        """
        Search for V-shaped diagonal segment.
        
        pattern_idx: 0 for expecting 2, 1 for expecting 0
        length: current length of the segment
        has_turned: whether we've already made a turn
        memo: memoization cache
        """
        # Create state for memoization
        state = (row, col, direction, pattern_idx, has_turned)
        if state in memo:
            return memo[state]
        
        # Define expected values in pattern: 2, 0, 2, 0, ...
        pattern = [2, 0]
        expected_val = pattern[pattern_idx]
        
        # Try to continue in the same direction
        dr, dc = directions[direction]
        next_row, next_col = row + dr, col + dc
        
        best_length = length
        
        if 0 <= next_row < n and 0 <= next_col < m:
            if grid[next_row][next_col] == expected_val:
                # Continue in same direction
                new_pattern_idx = 1 - pattern_idx
                result = self._search(grid, next_row, next_col, direction, directions, 
                                    new_pattern_idx, length + 1, n, m, has_turned, memo)
                best_length = max(best_length, result)
        
        # Try clockwise turn if:
        # 1. We haven't turned yet
        # 2. We've made at least 2 moves (starting cell + at least one move)
        if not has_turned and length > 1:
            # Try turning clockwise
            clockwise_dir = (direction + 1) % 4
            dr_turn, dc_turn = directions[clockwise_dir]
            turn_row, turn_col = row + dr_turn, col + dc_turn
            
            if 0 <= turn_row < n and 0 <= turn_col < m:
                if grid[turn_row][turn_col] == expected_val:
                    new_pattern_idx = 1 - pattern_idx
                    result = self._search(grid, turn_row, turn_col, clockwise_dir, directions,
                                        new_pattern_idx, length + 1, n, m, has_turned=True, memo=memo)
                    best_length = max(best_length, result)
        
        memo[state] = best_length
        return best_length


# Test with examples
if __name__ == "__main__":
    sol = Solution()
    
    # Example 1
    grid1 = [[2,2,1,2,2],[2,0,2,2,0],[2,0,1,1,0],[1,0,2,2,2],[2,0,0,2,2]]
    print("Example 1: {} (expected 5)".format(sol.lenOfVDiagonal(grid1)))
    
    # Example 2
    grid2 = [[2,2,2,2,2],[2,0,2,2,0],[2,0,1,1,0],[1,0,2,2,2],[2,0,0,2,2]]
    print("Example 2: {} (expected 4)".format(sol.lenOfVDiagonal(grid2)))
    
    # Example 3
    grid3 = [[1,2,2,2,2],[2,2,2,2,0],[2,0,0,0,0],[0,0,2,2,2],[2,0,0,2,0]]
    print("Example 3: {} (expected 5)".format(sol.lenOfVDiagonal(grid3)))
    
    # Example 4
    grid4 = [[1]]
    print("Example 4: {} (expected 1)".format(sol.lenOfVDiagonal(grid4)))
