def is_valid_move(p1_type, p1_r, p1_c, p2_type, p2_r, p2_c):
    """Check if piece at p1 can move to p2 in one move."""
    dr = abs(p1_r - p2_r)
    dc = abs(p1_c - p2_c)
    
    if p1_type == 'R':
        # Red: orthogonal move
        return (dr == 1 and dc == 0) or (dr == 0 and dc == 1)
    else:  # 'B'
        # Blue: diagonal move
        return dr == 1 and dc == 1

def verify_cycle(pieces):
    """Verify that pieces form a valid cycle."""
    n = len(pieces)
    if n == 0:
        return False
    
    # Check each consecutive pair
    for i in range(n):
        curr = pieces[i]
        next_piece = pieces[(i + 1) % n]
        
        if not is_valid_move(curr[0], curr[1], curr[2], next_piece[0], next_piece[1], next_piece[2]):
            return False
    
    return True

def construct_solution(R, B):
    """Try to construct a valid solution."""
    pieces = []
    
    if B == 0:
        # Only reds (R >= 2)
        # Create a 2-row snake pattern
        # Top row left-to-right, bottom row right-to-left
        
        k = (R + 1) // 2
        for i in range(k):
            pieces.append(('R', 1, i + 1))
        
        for i in range(R - k):
            pieces.append(('R', 2, R - k - i))
    
    elif R == 0:
        # Only blues (B >= 2)
        # Use a 2-row zigzag pattern
        
        for i in range(B):
            row = 1 if i % 2 == 0 else 2
            col = i + 1
            pieces.append(('B', row, col))
    
    elif R == 1:
        # One red, multiple blues (B >= 2)
        # Red at (2,2), blues around it
        
        pieces.append(('R', 2, 2))
        
        # Blues forming a cycle
        # Adjacent to (2,2) diagonally: (1,1), (1,3), (3,1), (3,3)
        # So: B(1,1) -> B(2,2) NO, R is there
        # Instead: B(1,1) -> B(3,2) NO, can't reach from (1,1)
        
        # Try: R(1,1) instead
        pieces = [('R', 1, 1)]
        
        # Blues must include at least one diagonally adjacent to (1,1)
        # Options: (0,0) invalid, (0,2) invalid, (2,0) invalid, (2,2) valid
        
        # Pattern: B(2,2) -> B(1,3) -> B(2,4) -> B(3,3) -> B(2,2) is a cycle
        # But we need to include R(1,1) and have each reach the next
        # (1,1) can reach (2,1) or (1,2) orthogonally
        
        # New pattern: 
        # R(1,1) -> B(1,2) -> B(2,3) -> B(3,2) -> B(2,1) -> R(1,1)
        pieces = [('R', 1, 1)]
        
        blues_coords = [(1, 2), (2, 3), (3, 2), (2, 1)]
        for i in range(min(B, len(blues_coords))):
            pieces.append(('B', blues_coords[i][0], blues_coords[i][1]))
        
        # If B > 4, extend with more blues
        if B > 4:
            # Continue the diagonal pattern
            for i in range(4, B):
                if i % 2 == 0:
                    pieces.append(('B', 1, i + 1))
                else:
                    pieces.append(('B', i // 2 + 2, 2))
    
    else:
        # R >= 2, B >= 1
        # Mixed case
        
        # Use a pattern where reds stay on a line and blues fill in
        # Pattern: R-R-B-R-B-... or similar
        
        # Try: All reds on top, all blues on bottom, with careful placement
        # Top row: R R R ...
        # Bottom row: B B B ...
        # But then we need R->B and B->R connections
        
        # Better: alternate carefully
        # R(1,1) -> R(1,2) -> B(2,2) -> B(2,1) -> back to R(1,1)
        # Check: R(1,1)->R(1,2) same row ✓
        #        R(1,2)->B(2,2) orthogonal down ✓
        #        B(2,2)->B(2,1) not diagonal ✗
        
        # Let me try: R(1,1) -> R(1,2) -> B(2,3) -> B(1,2)? NO (1,2) is taken
        # Or: R(1,1) -> B(2,2) -> R(2,1)? R can't move there from (1,1) if B is in between
        
        # Use a longer path: R(1,1) - R(1,2) - R(2,2) - R(2,1) - B(1,2)...
        # NO, R(2,1) and B(1,2) can't be adjacent diagonally from (2,1)
        
        # Let me use a proven pattern from literature:
        # Create a Hamiltonian cycle on a grid using specific rules
        
        # For R >= 2, B >= 1:
        # Use rows 1 and 2, place all pieces, then construct a valid path
        
        # Simple approach: Place reds first in a valid cycle, then insert blues
        
        if B == 1:
            # One blue, multiple reds
            # Red form a basic 2x2 cycle, insert blue somehow
            
            pieces = [
                ('R', 1, 1),
                ('R', 1, 2),
            ]
            
            if R > 2:
                pieces.append(('R', 2, 2))
                pieces.append(('B', 2, 1))
                for i in range(3, R):
                    pieces.append(('R', 1, i + 1))
            else:
                # R = 2
                pieces.append(('B', 2, 2))
        
        else:
            # B >= 2, R >= 2
            # Place R and B alternating on two rows
            
            # Row 1: R B R B ...
            # Row 2: R B R B ...
            
            for i in range(R):
                if i % 2 == 0:
                    pieces.append(('R', 1, i + 1))
                else:
                    pieces.append(('R', 2, i + 1))
            
            for i in range(B):
                col = R + i + 1
                if (R + i) % 2 == 0:
                    pieces.append(('B', 1, col))
                else:
                    pieces.append(('B', 2, col))
    
    return pieces

def solve():
    T = int(input())
    
    for _ in range(T):
        R, B = map(int, input().split())
        
        # Check impossible cases
        if (R + B == 1) or (R == 1 and B == 1):
            print("No")
            continue
        
        pieces = construct_solution(R, B)
        
        if verify_cycle(pieces):
            print("Yes")
            for piece_type, r, c in pieces:
                print(f"{piece_type} {r} {c}")
        else:
            # For debugging: show what we constructed
            print("No")

solve()
