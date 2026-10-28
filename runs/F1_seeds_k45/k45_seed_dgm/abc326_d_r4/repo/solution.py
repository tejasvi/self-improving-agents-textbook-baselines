def solve():
    N = int(input())
    R = input().strip()
    C = input().strip()
    
    # Grid to fill (None = empty, 'A', 'B', 'C')
    grid = [[None for _ in range(N)] for _ in range(N)]
    
    # Count of each character in each row and column
    row_count = [[0, 0, 0] for _ in range(N)]  # count of A, B, C
    col_count = [[0, 0, 0] for _ in range(N)]  # count of A, B, C
    
    # Track if each character has been placed in a row/column
    row_has = [[False, False, False] for _ in range(N)]  # has A, B, C
    col_has = [[False, False, False] for _ in range(N)]  # has A, B, C
    
    # Track leftmost and topmost in each row/column
    row_leftmost = [None] * N
    col_topmost = [None] * N
    
    def char_to_idx(c):
        return ord(c) - ord('A')
    
    def is_valid_placement(row, col, char):
        """Check if placing char at (row, col) is valid"""
        char_idx = char_to_idx(char)
        
        # Already have this character in this row/column
        if row_has[row][char_idx] or col_has[col][char_idx]:
            return False
        
        # If this would be the first character in this row
        if row_leftmost[row] is None and char != R[row]:
            return False
        
        # If this would be the first character in this column
        if col_topmost[col] is None and char != C[col]:
            return False
        
        return True
    
    def can_complete():
        """Check if remaining cells can be filled to satisfy constraints"""
        for i in range(N):
            # Each row needs all three characters
            chars_needed = []
            for c in range(3):
                if not row_has[i][c]:
                    chars_needed.append(chr(ord('A') + c))
            
            if row_leftmost[i] is None and len(chars_needed) > 0:
                # Need to place leftmost which must be R[i]
                if R[i] not in chars_needed:
                    return False
        
        for j in range(N):
            # Each column needs all three characters
            chars_needed = []
            for c in range(3):
                if not col_has[j][c]:
                    chars_needed.append(chr(ord('A') + c))
            
            if col_topmost[j] is None and len(chars_needed) > 0:
                # Need to place topmost which must be C[j]
                if C[j] not in chars_needed:
                    return False
        
        return True
    
    def backtrack(pos):
        """Backtrack through cells from position pos"""
        if not can_complete():
            return False
        
        if pos == N * N:
            # All cells filled, verify solution
            for i in range(N):
                count = [0, 0, 0]
                leftmost = None
                for j in range(N):
                    if grid[i][j] is not None:
                        count[char_to_idx(grid[i][j])] += 1
                        if leftmost is None:
                            leftmost = grid[i][j]
                if count != [1, 1, 1] or leftmost != R[i]:
                    return False
            
            for j in range(N):
                count = [0, 0, 0]
                topmost = None
                for i in range(N):
                    if grid[i][j] is not None:
                        count[char_to_idx(grid[i][j])] += 1
                        if topmost is None:
                            topmost = grid[i][j]
                if count != [1, 1, 1] or topmost != C[j]:
                    return False
            
            return True
        
        row = pos // N
        col = pos % N
        
        # Try leaving empty
        if backtrack(pos + 1):
            return True
        
        # Try placing each character
        for char in ['A', 'B', 'C']:
            if is_valid_placement(row, col, char):
                char_idx = char_to_idx(char)
                
                # Place character
                grid[row][col] = char
                row_has[row][char_idx] = True
                col_has[col][char_idx] = True
                row_count[row][char_idx] += 1
                col_count[col][char_idx] += 1
                
                if row_leftmost[row] is None:
                    row_leftmost[row] = char
                if col_topmost[col] is None:
                    col_topmost[col] = char
                
                if backtrack(pos + 1):
                    return True
                
                # Backtrack
                grid[row][col] = None
                row_has[row][char_idx] = False
                col_has[col][char_idx] = False
                row_count[row][char_idx] -= 1
                col_count[col][char_idx] -= 1
                
                # Only reset leftmost if this was the only one
                if row_count[row][char_idx] == 0:
                    row_leftmost[row] = None
                if col_count[col][char_idx] == 0:
                    col_topmost[col] = None
        
        return False
    
    if backtrack(0):
        print("Yes")
        for i in range(N):
            row_str = ""
            for j in range(N):
                if grid[i][j] is None:
                    row_str += "."
                else:
                    row_str += grid[i][j]
            print(row_str)
    else:
        print("No")

solve()
