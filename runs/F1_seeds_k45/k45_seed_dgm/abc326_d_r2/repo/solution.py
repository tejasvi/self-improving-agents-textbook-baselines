def solve():
    N = int(input())
    R = input().strip()
    C = input().strip()
    
    # Grid: 0 = empty, 1 = A, 2 = B, 3 = C
    grid = [[0] * N for _ in range(N)]
    
    # Track which characters are placed in each row and column
    row_chars = [set() for _ in range(N)]
    col_chars = [set() for _ in range(N)]
    
    # Track leftmost position in each row and topmost in each column
    row_leftmost = [None] * N
    col_topmost = [None] * N
    
    def char_to_num(ch):
        if ch == 'A':
            return 1
        elif ch == 'B':
            return 2
        else:  # ch == 'C'
            return 3
    
    def num_to_char(num):
        if num == 0:
            return '.'
        elif num == 1:
            return 'A'
        elif num == 2:
            return 'B'
        else:  # num == 3
            return 'C'
    
    def can_place(r, c, num):
        # Check if we already have this character in this row/column
        if num in row_chars[r] or num in col_chars[c]:
            return False
        return True
    
    def update_leftmost(r, c):
        if row_leftmost[r] is None:
            row_leftmost[r] = c
    
    def update_topmost(c, r):
        if col_topmost[c] is None:
            col_topmost[c] = r
    
    def is_valid_partial():
        # Check if leftmost constraints can still be satisfied
        for r in range(N):
            if row_leftmost[r] is not None:
                expected_char = char_to_num(R[r])
                actual_char = grid[r][row_leftmost[r]]
                if actual_char != 0 and actual_char != expected_char:
                    return False
        
        # Check if topmost constraints can still be satisfied
        for c in range(N):
            if col_topmost[c] is not None:
                expected_char = char_to_num(C[c])
                actual_char = grid[col_topmost[c]][c]
                if actual_char != 0 and actual_char != expected_char:
                    return False
        
        return True
    
    def backtrack(pos):
        if not is_valid_partial():
            return False
        
        if pos == N * N:
            # Check all constraints are satisfied
            for r in range(N):
                if row_leftmost[r] is None or len(row_chars[r]) != 3:
                    return False
            for c in range(N):
                if col_topmost[c] is None or len(col_chars[c]) != 3:
                    return False
            
            # Verify leftmost and topmost constraints
            for r in range(N):
                expected = char_to_num(R[r])
                actual = grid[r][row_leftmost[r]]
                if actual != expected:
                    return False
            
            for c in range(N):
                expected = char_to_num(C[c])
                actual = grid[col_topmost[c]][c]
                if actual != expected:
                    return False
            
            return True
        
        r = pos // N
        c = pos % N
        
        # Try placing each character or leaving empty
        for num in [0, 1, 2, 3]:
            if num == 0:
                # Leave empty
                grid[r][c] = 0
                if backtrack(pos + 1):
                    return True
                grid[r][c] = 0
            else:
                # Try to place this character
                if can_place(r, c, num):
                    grid[r][c] = num
                    row_chars[r].add(num)
                    col_chars[c].add(num)
                    
                    if row_leftmost[r] is None:
                        update_leftmost(r, c)
                    if col_topmost[c] is None:
                        update_topmost(c, r)
                    
                    if backtrack(pos + 1):
                        return True
                    
                    # Undo
                    grid[r][c] = 0
                    row_chars[r].discard(num)
                    col_chars[c].discard(num)
        
        return False
    
    if backtrack(0):
        print("Yes")
        for r in range(N):
            print(''.join(num_to_char(grid[r][c]) for c in range(N)))
    else:
        print("No")

solve()
