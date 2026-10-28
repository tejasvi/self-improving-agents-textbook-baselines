def solve():
    N = int(input())
    R = input().strip()
    C = input().strip()
    
    def is_valid_solution(grid):
        """Check if a completed grid is a valid solution"""
        # Each row and column must have exactly one A, B, C
        for i in range(N):
            row_chars = set()
            for j in range(N):
                if grid[i][j] != '.':
                    row_chars.add(grid[i][j])
            if row_chars != {'A', 'B', 'C'}:
                return False
        
        for j in range(N):
            col_chars = set()
            for i in range(N):
                if grid[i][j] != '.':
                    col_chars.add(grid[i][j])
            if col_chars != {'A', 'B', 'C'}:
                return False
        
        # Check leftmost constraints
        for i in range(N):
            leftmost_char = None
            for j in range(N):
                if grid[i][j] != '.':
                    leftmost_char = grid[i][j]
                    break
            if leftmost_char != R[i]:
                return False
        
        # Check topmost constraints
        for j in range(N):
            topmost_char = None
            for i in range(N):
                if grid[i][j] != '.':
                    topmost_char = grid[i][j]
                    break
            if topmost_char != C[j]:
                return False
        
        return True
    
    # Track placed characters
    row_chars = [set() for _ in range(N)]
    col_chars = [set() for _ in range(N)]
    grid = [['.' for _ in range(N)] for _ in range(N)]
    
    # Track leftmost position in each row and topmost in each column
    leftmost_in_row = [N] * N  # Position of leftmost char in row i
    topmost_in_col = [N] * N   # Position of topmost char in col j
    
    def can_place(i, j, char):
        # Cell already filled
        if grid[i][j] != '.':
            return False
        
        # Character already in this row
        if char in row_chars[i]:
            return False
        
        # Character already in this column
        if char in col_chars[j]:
            return False
        
        # Check leftmost constraint
        if j < leftmost_in_row[i]:
            # This would become the leftmost character in the row
            if char != R[i]:
                return False
        
        # Check topmost constraint
        if i < topmost_in_col[j]:
            # This would become the topmost character in the column
            if char != C[j]:
                return False
        
        return True
    
    def backtrack(cell_idx):
        if cell_idx == N * N:
            return is_valid_solution(grid)
        
        i = cell_idx // N
        j = cell_idx % N
        
        # Early termination: if a row already has all 3 chars, we can skip remaining cells in this row
        if len(row_chars[i]) == 3:
            # Skip to next row
            next_row_cell = ((i + 1) * N)
            return backtrack(next_row_cell)
        
        # Early termination: if we've filled enough cells and there are remaining unfilled rows
        # that still need characters, we must place at least one character in remaining cells of this row
        
        # Try each character first (more likely to lead to a solution)
        for char in ['A', 'B', 'C']:
            if can_place(i, j, char):
                grid[i][j] = char
                row_chars[i].add(char)
                col_chars[j].add(char)
                
                # Update leftmost and topmost
                old_leftmost = leftmost_in_row[i]
                old_topmost = topmost_in_col[j]
                
                if j < leftmost_in_row[i]:
                    leftmost_in_row[i] = j
                if i < topmost_in_col[j]:
                    topmost_in_col[j] = i
                
                if backtrack(cell_idx + 1):
                    return True
                
                # Restore
                grid[i][j] = '.'
                row_chars[i].discard(char)
                col_chars[j].discard(char)
                leftmost_in_row[i] = old_leftmost
                topmost_in_col[j] = old_topmost
        
        # Try empty last
        if backtrack(cell_idx + 1):
            return True
        
        return False
    
    if backtrack(0):
        print("Yes")
        for row in grid:
            print(''.join(row))
    else:
        print("No")

solve()
