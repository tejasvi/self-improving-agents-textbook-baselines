# Write your solution here. Read from stdin, write to stdout.

def solve_abc_puzzle():
    N = int(input())
    R = input().strip()
    C = input().strip()
    
    # Convert character to index
    def char_to_idx(c):
        return ord(c) - ord('A')
    
    # Convert index to character
    def idx_to_char(idx):
        return chr(ord('A') + idx)
    
    # Grid to store the solution (-1 = empty, 0 = A, 1 = B, 2 = C)
    grid = [[-1] * N for _ in range(N)]
    
    # Track which characters are placed in each row and column
    row_chars = [set() for _ in range(N)]
    col_chars = [set() for _ in range(N)]
    
    def find_leftmost_in_row(row):
        """Find the leftmost character in a row"""
        for col in range(N):
            if grid[row][col] != -1:
                return grid[row][col]
        return None
    
    def find_topmost_in_col(col):
        """Find the topmost character in a column"""
        for row in range(N):
            if grid[row][col] != -1:
                return grid[row][col]
        return None
    
    def is_valid():
        """Check if current state is valid"""
        # Check all rows
        for i in range(N):
            # No character should exceed the leftmost requirement
            leftmost = find_leftmost_in_row(i)
            if leftmost is not None and leftmost != char_to_idx(R[i]):
                return False
            # Can't have more than 3 characters per row
            if len(row_chars[i]) > 3:
                return False
        
        # Check all columns
        for j in range(N):
            # No character should exceed the topmost requirement
            topmost = find_topmost_in_col(j)
            if topmost is not None and topmost != char_to_idx(C[j]):
                return False
            # Can't have more than 3 characters per column
            if len(col_chars[j]) > 3:
                return False
        
        return True
    
    def is_complete():
        """Check if solution is complete and valid"""
        # Each row must have exactly A, B, C
        for i in range(N):
            if len(row_chars[i]) != 3:
                return False
            leftmost = find_leftmost_in_row(i)
            if leftmost != char_to_idx(R[i]):
                return False
        
        # Each column must have exactly A, B, C
        for j in range(N):
            if len(col_chars[j]) != 3:
                return False
            topmost = find_topmost_in_col(j)
            if topmost != char_to_idx(C[j]):
                return False
        
        return True
    
    def backtrack(cell_idx):
        """Try to fill the grid using backtracking"""
        # All cells processed
        if cell_idx == N * N:
            return is_complete()
        
        row = cell_idx // N
        col = cell_idx % N
        
        # Try placing each character or leaving empty
        for char_idx in [-1, 0, 1, 2]:  # empty, A, B, C
            if char_idx != -1:
                # Check if character already in row or column
                if char_idx in row_chars[row] or char_idx in col_chars[col]:
                    continue
            
            # Place/leave empty
            grid[row][col] = char_idx
            if char_idx != -1:
                row_chars[row].add(char_idx)
                col_chars[col].add(char_idx)
            
            # Check validity
            if is_valid():
                # Additional pruning: if this is the first character, verify constraint
                if char_idx != -1:
                    if find_leftmost_in_row(row) == char_idx:
                        if char_idx != char_to_idx(R[row]):
                            grid[row][col] = -1
                            row_chars[row].discard(char_idx)
                            col_chars[col].discard(char_idx)
                            continue
                    
                    if find_topmost_in_col(col) == char_idx:
                        if char_idx != char_to_idx(C[col]):
                            grid[row][col] = -1
                            row_chars[row].discard(char_idx)
                            col_chars[col].discard(char_idx)
                            continue
                
                if backtrack(cell_idx + 1):
                    return True
            
            # Backtrack
            if char_idx != -1:
                row_chars[row].discard(char_idx)
                col_chars[col].discard(char_idx)
            grid[row][col] = -1
        
        return False
    
    # Try to find a solution
    if backtrack(0):
        print("Yes")
        for row in range(N):
            line = ""
            for col in range(N):
                if grid[row][col] == -1:
                    line += "."
                else:
                    line += idx_to_char(grid[row][col])
            print(line)
    else:
        print("No")

solve_abc_puzzle()
