def solve():
    N = int(input())
    R = input().strip()
    C = input().strip()
    
    # Initialize grid
    grid = [['.' for _ in range(N)] for _ in range(N)]
    
    # Track which characters are placed in each row and column
    row_chars = [set() for _ in range(N)]
    col_chars = [set() for _ in range(N)]
    
    # Track the position of the first non-empty cell in each row and column
    row_first = [-1] * N  # -1 means not yet placed
    col_first = [-1] * N
    
    def is_valid(r, c, ch):
        # Check if placing 'ch' at (r, c) is valid
        
        # Already has this character in row or column
        if ch in row_chars[r] or ch in col_chars[c]:
            return False
        
        # If this would be the first character in the row, check if it matches R[r]
        if row_first[r] == -1 and ch != R[r]:
            return False
        
        # If this would be the first character in the column, check if it matches C[c]
        if col_first[c] == -1 and ch != C[c]:
            return False
        
        return True
    
    def backtrack(pos):
        # pos is the cell index (0 to N*N-1)
        
        # If we've filled all cells, check if solution is valid
        if pos == N * N:
            # Check that each row has exactly one A, B, C
            for i in range(N):
                if len(row_chars[i]) != 3:
                    return False
            # Check that each column has exactly one A, B, C
            for j in range(N):
                if len(col_chars[j]) != 3:
                    return False
            return True
        
        r = pos // N
        c = pos % N
        
        # Pruning: if we've reached max chars for row/col, cell must be empty
        if len(row_chars[r]) == 3 or len(col_chars[c]) == 3:
            return backtrack(pos + 1)
        
        # Try leaving the cell empty
        if backtrack(pos + 1):
            return True
        
        # Try placing A, B, C
        for ch in ['A', 'B', 'C']:
            if is_valid(r, c, ch):
                # Place the character
                grid[r][c] = ch
                row_chars[r].add(ch)
                col_chars[c].add(ch)
                
                # Update first positions
                old_row_first = row_first[r]
                old_col_first = col_first[c]
                
                if row_first[r] == -1:
                    row_first[r] = c
                if col_first[c] == -1:
                    col_first[c] = r
                
                if backtrack(pos + 1):
                    return True
                
                # Backtrack
                grid[r][c] = '.'
                row_chars[r].remove(ch)
                col_chars[c].remove(ch)
                row_first[r] = old_row_first
                col_first[c] = old_col_first
        
        return False
    
    if backtrack(0):
        print("Yes")
        for row in grid:
            print(''.join(row))
    else:
        print("No")

solve()
