def solve():
    N = int(input())
    R = input().strip()
    C = input().strip()
    
    # Grid representation: grid[i][j] contains the character or '.' for empty
    grid = [['.' for _ in range(N)] for _ in range(N)]
    
    # Track which characters are placed in each row and column
    row_chars = [set() for _ in range(N)]  # Characters already in each row
    col_chars = [set() for _ in range(N)]  # Characters already in each column
    
    # Track the position of leftmost char in each row
    row_leftmost_pos = [-1] * N
    # Track the position of topmost char in each column
    col_topmost_pos = [-1] * N
    
    def is_valid():
        """Check if current state is valid"""
        # Check row constraints
        for i in range(N):
            if len(row_chars[i]) > 3:
                return False
            if row_leftmost_pos[i] != -1:
                # Check if leftmost character matches R[i]
                if grid[i][row_leftmost_pos[i]] != R[i]:
                    return False
            elif len(row_chars[i]) > 0:
                # Has characters but no leftmost set yet - shouldn't happen
                return False
        
        # Check column constraints
        for j in range(N):
            if len(col_chars[j]) > 3:
                return False
            if col_topmost_pos[j] != -1:
                # Check if topmost character matches C[j]
                if grid[col_topmost_pos[j]][j] != C[j]:
                    return False
            elif len(col_chars[j]) > 0:
                # Has characters but no topmost set yet - shouldn't happen
                return False
        
        return True
    
    def is_complete():
        """Check if the grid is complete and valid"""
        for i in range(N):
            if len(row_chars[i]) != 3:
                return False
            if row_leftmost_pos[i] == -1:
                return False
            if grid[i][row_leftmost_pos[i]] != R[i]:
                return False
        
        for j in range(N):
            if len(col_chars[j]) != 3:
                return False
            if col_topmost_pos[j] == -1:
                return False
            if grid[col_topmost_pos[j]][j] != C[j]:
                return False
        
        return True
    
    def backtrack(row, col):
        """Backtracking solver"""
        if row == N:
            return is_complete()
        
        next_row, next_col = (row, col + 1) if col + 1 < N else (row + 1, 0)
        
        # Try placing each character or empty
        for char in ['.', 'A', 'B', 'C']:
            if char == '.':
                # Leave empty
                if is_valid() and backtrack(next_row, next_col):
                    return True
            else:
                # Try placing this character
                if char in row_chars[row]:
                    # Already have this char in row
                    continue
                if char in col_chars[col]:
                    # Already have this char in column
                    continue
                
                # Place the character
                grid[row][col] = char
                row_chars[row].add(char)
                col_chars[col].add(char)
                
                # Update leftmost position in row
                old_row_leftmost = row_leftmost_pos[row]
                if row_leftmost_pos[row] == -1:
                    row_leftmost_pos[row] = col
                
                # Update topmost position in column
                old_col_topmost = col_topmost_pos[col]
                if col_topmost_pos[col] == -1:
                    col_topmost_pos[col] = row
                
                if is_valid() and backtrack(next_row, next_col):
                    return True
                
                # Backtrack
                grid[row][col] = '.'
                row_chars[row].remove(char)
                col_chars[col].remove(char)
                row_leftmost_pos[row] = old_row_leftmost
                col_topmost_pos[col] = old_col_topmost
        
        return False
    
    if backtrack(0, 0):
        print("Yes")
        for row in grid:
            print(''.join(row))
    else:
        print("No")

solve()
