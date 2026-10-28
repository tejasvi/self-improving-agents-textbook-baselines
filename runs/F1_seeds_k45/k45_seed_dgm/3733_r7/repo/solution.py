class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        """
        Find the longest V-shaped diagonal segment in the grid.
        
        The segment:
        1. Starts with value 1
        2. Follows sequence 2, 0, 2, 0, ... in diagonal direction
        3. Can optionally make ONE clockwise 90-degree turn
        """
        if not grid or not grid[0]:
            return 0
        
        n, m = len(grid), len(grid[0])
        max_length = 0
        
        # Four diagonal directions: (dr, dc)
        # (1,1): top-left to bottom-right
        # (1,-1): top-right to bottom-left
        # (-1,-1): bottom-right to top-left
        # (-1,1): bottom-left to top-right
        directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        
        # Clockwise turn mapping: from current direction to next direction after clockwise 90-degree turn
        # (1,1) -> (1,-1) (downright to downleft)
        # (1,-1) -> (-1,-1) (downleft to upleft)
        # (-1,-1) -> (-1,1) (upleft to upright)
        # (-1,1) -> (1,1) (upright to downright)
        clockwise_turn = {
            (1, 1): (1, -1),
            (1, -1): (-1, -1),
            (-1, -1): (-1, 1),
            (-1, 1): (1, 1)
        }
        
        # Try starting from each cell that contains 1
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 1:
                    # Try each of the 4 diagonal directions
                    for dr, dc in directions:
                        length = self._dfs(grid, i, j, dr, dc, -1, 0, False, clockwise_turn)
                        max_length = max(max_length, length)
        
        return max_length
    
    def _dfs(self, grid, r, c, dr, dc, expected_value, length, turned, clockwise_turn):
        """
        DFS helper to find V-shaped diagonal segment.
        
        Args:
            grid: The grid
            r, c: Current position
            dr, dc: Current direction
            expected_value: The value we expect at (r, c). Start with -1 (will be 1).
            length: Current length of segment
            turned: Whether we've already made a turn
            clockwise_turn: Mapping of clockwise turns
        
        Returns:
            Maximum length achievable from this state
        """
        n, m = len(grid), len(grid[0])
        
        # Check bounds
        if r < 0 or r >= n or c < 0 or c >= m:
            return length
        
        # Check if current value matches expected
        if length == 0:
            # First cell must be 1
            if grid[r][c] != 1:
                return 0
        else:
            # Expected value cycles through 2, 0, 2, 0, ...
            if grid[r][c] != expected_value:
                return length
        
        # Calculate next expected value
        if length == 0:
            next_expected = 2
        else:
            next_expected = 2 if expected_value == 0 else 0
        
        # Move in current direction
        nr, nc = r + dr, c + dc
        
        max_len = length + 1
        
        # Continue in same direction
        if 0 <= nr < n and 0 <= nc < m:
            continued = self._dfs(grid, nr, nc, dr, dc, next_expected, length + 1, turned, clockwise_turn)
            max_len = max(max_len, continued)
        
        # Try clockwise turn if we haven't turned yet
        if not turned:
            new_dir = clockwise_turn[(dr, dc)]
            nr, nc = r + new_dir[0], c + new_dir[1]
            if 0 <= nr < n and 0 <= nc < m:
                turned_result = self._dfs(grid, nr, nc, new_dir[0], new_dir[1], next_expected, length + 1, True, clockwise_turn)
                max_len = max(max_len, turned_result)
        
        return max_len
