def solve():
    n = int(input())
    R = input().strip()
    C = input().strip()
    
    # Grid: grid[i][j] is character at position (i,j), or None if empty
    grid = [[None] * n for _ in range(n)]
    
    # Track which characters are used in each row and column
    row_chars = [set() for _ in range(n)]
    col_chars = [set() for _ in range(n)]
    
    # Track the leftmost non-empty column in each row
    row_leftmost_col = [None] * n
    # Track the topmost non-empty row in each column
    col_topmost_row = [None] * n
    
    def is_complete():
        """Check if current state is a complete solution"""
        for r in range(n):
            if len(row_chars[r]) != 3 or row_leftmost_col[r] is None:
                return False
        for c in range(n):
            if len(col_chars[c]) != 3 or col_topmost_row[c] is None:
                return False
        return True
    
    def can_complete():
        """Check if current state can potentially be completed"""
        for r in range(n):
            if len(row_chars[r]) > 3:
                return False
            if row_leftmost_col[r] is not None and row_leftmost_col[r] >= n:
                return False
        for c in range(n):
            if len(col_chars[c]) > 3:
                return False
            if col_topmost_row[c] is not None and col_topmost_row[c] >= n:
                return False
        return True
    
    def solve_recursive(cell_idx):
        """
        Try to fill cells in order from (0,0) to (n-1, n-1).
        cell_idx is the current cell index in row-major order.
        """
        if cell_idx == n * n:
            return is_complete()
        
        # Early pruning
        if not can_complete():
            return False
        
        row = cell_idx // n
        col = cell_idx % n
        
        # Try leaving cell empty
        if solve_recursive(cell_idx + 1):
            return True
        
        # Try placing each character
        for char in ['A', 'B', 'C']:
            # Check if char is already in this row or column
            if char in row_chars[row] or char in col_chars[col]:
                continue
            
            # Check row leftmost constraint
            if row_leftmost_col[row] is None:
                # This would be the leftmost char in this row
                if char != R[row]:
                    continue
                
                # Check column topmost constraint
                if col_topmost_row[col] is None:
                    # This would be the topmost char in this column
                    if char != C[col]:
                        continue
                    col_topmost_row[col] = row
                
                grid[row][col] = char
                row_chars[row].add(char)
                col_chars[col].add(char)
                row_leftmost_col[row] = col
                
                if solve_recursive(cell_idx + 1):
                    return True
                
                grid[row][col] = None
                row_chars[row].remove(char)
                col_chars[col].remove(char)
                row_leftmost_col[row] = None
                if col_topmost_row[col] == row:
                    col_topmost_row[col] = None
            else:
                # This is not the leftmost char in this row
                # Check column topmost constraint
                if col_topmost_row[col] is None:
                    # This would be the topmost char in this column
                    if char != C[col]:
                        continue
                    col_topmost_row[col] = row
                
                grid[row][col] = char
                row_chars[row].add(char)
                col_chars[col].add(char)
                
                if solve_recursive(cell_idx + 1):
                    return True
                
                grid[row][col] = None
                row_chars[row].remove(char)
                col_chars[col].remove(char)
                if col_topmost_row[col] == row:
                    col_topmost_row[col] = None
        
        return False
    
    if solve_recursive(0):
        print("Yes")
        for row in grid:
            print(''.join(cell if cell else '.' for cell in row))
    else:
        print("No")

solve()
