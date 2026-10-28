def solve():
    N = int(input())
    R = input().strip()
    C = input().strip()
    
    # Grid: 0 = empty, 1 = A, 2 = B, 3 = C
    grid = [[0 for _ in range(N)] for _ in range(N)]
    
    # For each row/col, track which characters are already placed
    row_has = [[False] * 4 for _ in range(N)]  # row_has[r][0] unused, [1]=A, [2]=B, [3]=C
    col_has = [[False] * 4 for _ in range(N)]
    
    # Track leftmost and topmost positions
    row_leftmost = [-1] * N
    col_topmost = [-1] * N
    
    def char_to_int(ch):
        return ord(ch) - ord('A') + 1
    
    def int_to_char(i):
        if i == 0:
            return '.'
        return chr(i - 1 + ord('A'))
    
    def can_place(r, c, ch_int):
        return not row_has[r][ch_int] and not col_has[c][ch_int]
    
    def place(r, c, ch_int):
        grid[r][c] = ch_int
        row_has[r][ch_int] = True
        col_has[c][ch_int] = True
        
        if row_leftmost[r] == -1:
            row_leftmost[r] = c
        if col_topmost[c] == -1:
            col_topmost[c] = r
    
    def unplace(r, c, ch_int):
        grid[r][c] = 0
        row_has[r][ch_int] = False
        col_has[c][ch_int] = False
        
        # Recalculate leftmost
        if row_leftmost[r] == c:
            row_leftmost[r] = -1
            for j in range(N):
                if grid[r][j] != 0:
                    row_leftmost[r] = j
                    break
        
        # Recalculate topmost
        if col_topmost[c] == r:
            col_topmost[c] = -1
            for i in range(N):
                if grid[i][c] != 0:
                    col_topmost[c] = i
                    break
    
    def check_constraints():
        """Check if current placement satisfies constraints"""
        for r in range(N):
            if row_leftmost[r] != -1:
                r_int = char_to_int(R[r])
                if grid[r][row_leftmost[r]] != r_int:
                    return False
        
        for c in range(N):
            if col_topmost[c] != -1:
                c_int = char_to_int(C[c])
                if grid[col_topmost[c]][c] != c_int:
                    return False
        
        return True
    
    def is_complete():
        """Check if solution is complete and valid"""
        for r in range(N):
            count = sum(1 for ch_int in range(1, 4) if row_has[r][ch_int])
            if count != 3:
                return False
        
        for c in range(N):
            count = sum(1 for ch_int in range(1, 4) if col_has[c][ch_int])
            if count != 3:
                return False
        
        return check_constraints()
    
    def backtrack(pos):
        """Backtrack through grid positions"""
        if pos == N * N:
            return is_complete()
        
        r = pos // N
        c = pos % N
        
        # Try leaving empty
        if check_constraints():
            if backtrack(pos + 1):
                return True
        
        # Try placing A, B, C
        for ch_int in range(1, 4):
            if can_place(r, c, ch_int):
                # Additional check: don't exceed 3 per row/col
                row_count = sum(1 for x in range(1, 4) if row_has[r][x])
                col_count = sum(1 for x in range(1, 4) if col_has[c][x])
                
                if row_count < 3 and col_count < 3:
                    place(r, c, ch_int)
                    
                    if check_constraints():
                        if backtrack(pos + 1):
                            return True
                    
                    unplace(r, c, ch_int)
        
        return False
    
    if backtrack(0):
        print("Yes")
        for r in range(N):
            row_str = ""
            for c in range(N):
                row_str += int_to_char(grid[r][c])
            print(row_str)
    else:
        print("No")

solve()
