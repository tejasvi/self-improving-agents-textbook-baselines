def solve(R, B):
    total = R + B
    
    # Case 1: Only red pieces (B = 0)
    if B == 0:
        if R >= 2:
            result = []
            # Create a rectangular path with red pieces
            if R == 2:
                # Simple path: (1,1) -> (1,2) -> (1,1)
                result = [
                    ('R', 1, 1),
                    ('R', 1, 2),
                ]
            else:
                # Make a 2xN rectangle path
                # (1,1) -> (1,2) -> ... -> (1,R) -> (2,R) -> (2,R-1) -> ... -> (2,1) -> (1,1)
                result = []
                # Top row left to right
                for c in range(1, R + 1):
                    result.append(('R', 1, c))
                # Bottom row right to left
                for c in range(R, 0, -1):
                    result.append(('R', 2, c))
            
            return result
        else:
            return None
    
    # Case 2: Only blue pieces (R = 0)
    elif R == 0:
        # Blue pieces need at least 4 pieces and need even number
        # This is tricky - blue pieces move diagonally
        return None
    
    # Case 3: Mixed pieces (R >= 1, B >= 1)
    else:
        # Single red or single blue is problematic
        if R == 1 or B == 1:
            return None
        
        # For R >= 2, B >= 2:
        if R >= 2 and B >= 2:
            # We can create a pattern where reds and blues alternate
            # Key insight: we need reds to connect to blues and vice versa
            
            result = []
            
            # Use a rectangular spiral pattern
            # Place pieces alternating on a 2x(R+B)/2 grid
            
            # Simple approach: create two rows
            # Row 1: pieces going left to right
            # Row 2: pieces going right to left
            
            # Pattern that works:
            # (1,1)R -> (2,1)B -> (2,2)R -> (1,2)B -> (1,3)R -> (2,3)B -> ... -> back to (1,1)
            
            # Or simpler: make a 2x((R+B)/2) grid with alternating pattern
            
            result = []
            
            # Ensure R and B are both at least 2
            # Create a checkerboard pattern on a rectangle
            
            col = 1
            
            # First, try to place pieces alternating R and B in a way that forms a cycle
            # For simplicity, use a rectangular path
            
            # Place pieces in a specific pattern
            # (1,1), (1,2), (1,3), ..., (2,n), (2,n-1), ..., (2,1)
            # and assign R/B to alternate as much as possible
            
            # Simple: 2x(R+B)//2 grid with carefully chosen R/B placement
            
            positions = []
            
            # Row 1: left to right for (R+B)//2 + 1 positions
            for c in range(1, (R + B) // 2 + 2):
                positions.append((1, c))
            
            # Row 2: right to left
            for c in range((R + B) // 2 + 1, 0, -1):
                positions.append((2, c))
            
            # Now assign R and B to positions to ensure cycle validity
            # We need reds to connect to blues or vice versa
            
            # Strategy: alternate R and B, but adjust for specific counts
            
            used_r = 0
            used_b = 0
            
            for i, (r, c) in enumerate(positions):
                if i < len(positions):
                    # Alternate for as long as we can
                    if i % 2 == 0 and used_r < R:
                        result.append(('R', r, c))
                        used_r += 1
                    elif used_b < B:
                        result.append(('B', r, c))
                        used_b += 1
                    elif used_r < R:
                        result.append(('R', r, c))
                        used_r += 1
            
            if len(result) == R + B:
                return result
            
            return None
        
        return None
    
    return None


def verify_solution(pieces):
    """Verify that a solution forms a valid Hamiltonian cycle"""
    if len(pieces) < 2:
        return False
    
    n = len(pieces)
    
    for i in range(n):
        curr_type, curr_r, curr_c = pieces[i]
        next_idx = (i + 1) % n
        next_type, next_r, next_c = pieces[next_idx]
        
        can_reach = False
        
        if curr_type == 'R':
            # Red pieces move orthogonally
            if (abs(curr_r - next_r) == 1 and curr_c == next_c) or \
               (abs(curr_c - next_c) == 1 and curr_r == next_r):
                can_reach = True
        else:  # curr_type == 'B'
            # Blue pieces move diagonally
            if abs(curr_r - next_r) == 1 and abs(curr_c - next_c) == 1:
                can_reach = True
        
        if not can_reach:
            return False
    
    return True


def main():
    T = int(input())
    for _ in range(T):
        R, B = map(int, input().split())
        result = solve(R, B)
        
        if result is None:
            print("No")
        else:
            print("Yes")
            for p, r, c in result:
                print(f"{p} {r} {c}")


if __name__ == "__main__":
    main()
