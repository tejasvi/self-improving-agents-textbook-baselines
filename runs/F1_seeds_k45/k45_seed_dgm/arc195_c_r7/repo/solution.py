# Write your solution here. Read from stdin, write to stdout.

def solve(R, B):
    total = R + B
    
    # Impossible case: exactly 1 red and 1 blue
    if R == 1 and B == 1:
        return None
    
    pieces = []
    
    # Case 1: Only red pieces (B = 0)
    if B == 0:
        # Create a rectangular cycle with reds
        # Pattern: (1,1) -> (1,2) -> (2,2) -> (2,1) -> (1,1)
        # For more reds, extend the pattern
        pieces = []
        r = 1
        c = 1
        for i in range(R):
            pieces.append(('R', r, c))
            if i < R - 1:
                # Move to next position in a snake pattern
                if r == 1 and c == 1:
                    c = 2
                elif r == 1 and c == 2:
                    r = 2
                elif r == 2 and c == 2:
                    c = 1
                elif r == 2 and c == 1:
                    r = 3
                    c = 1
                elif r >= 3:
                    if c == 1:
                        c = 2
                    else:
                        r += 1
                        c = 1
    
    # Case 2: Only blue pieces (R = 0)
    elif R == 0:
        # Create a cycle with blues moving diagonally
        # A blue at (r,c) can move to (r±1, c±1)
        # Pattern: (1,1) -> (2,2) -> (1,3) -> (2,4) -> ...
        # Or simpler: (1,1) -> (2,2) -> (3,1) -> (4,2) -> (5,1) -> back to (1,1)
        pieces = []
        for i in range(B):
            if i % 2 == 0:
                r = 1 + i // 2
                c = 1
            else:
                r = 1 + i // 2
                c = 2
            pieces.append(('B', r, c))
    
    # Case 3: Both red and blue pieces
    else:
        pieces = []
        
        if R == 1:
            # R=1, B>=2
            # Red at (1,1)
            # Blue at (1,2) - can reach (1,1)
            # Blue at (2,1) or (2,3) - can reach back to red
            # Then continue with other blues
            pieces.append(('R', 1, 1))
            pieces.append(('B', 1, 2))
            pieces.append(('B', 2, 1))
            
            # Add more blues if needed
            for i in range(3, B + 1):
                r = 2 + (i - 3) // 2
                c = 1 + (i - 3) % 2
                pieces.append(('B', r, c))
        
        elif B == 1:
            # R>=2, B=1
            # Blue at (1,1)
            # Red at (1,2) or (2,1) - can reach blue diagonally? NO! Red can't reach blue from (1,2) to (1,1)
            # So: Blue at (1,1), Red at (2,2) - Red can't reach Blue diagonally
            # Strategy: Blue at (1,1), Red at (1,2), Red at (2,2), Red at (2,1)...
            pieces.append(('B', 1, 1))
            pieces.append(('R', 1, 2))
            
            # Continue with more reds
            r, c = 1, 2
            for i in range(1, R):
                if i == 1:
                    r, c = 2, 2
                elif i % 2 == 0:
                    c -= 1
                else:
                    r += 1
                pieces.append(('R', r, c))
        
        else:
            # Both R>=2 and B>=2
            # Create a pattern that alternates or interleaves properly
            # Strategy: use a rectangular grid
            pieces = []
            
            # Build a simple alternating path
            # (1,1)R -> (1,2)B -> (2,2)R -> (2,1)B -> (3,1)R -> ...
            r, c = 1, 1
            red_used = 0
            blue_used = 0
            
            for i in range(total):
                if i % 4 == 0:  # Top-left: place Red if available
                    if red_used < R:
                        pieces.append(('R', r, c))
                        red_used += 1
                    else:
                        pieces.append(('B', r, c))
                        blue_used += 1
                elif i % 4 == 1:  # Top-right: place Blue if available
                    c += 1
                    if blue_used < B:
                        pieces.append(('B', r, c))
                        blue_used += 1
                    else:
                        pieces.append(('R', r, c))
                        red_used += 1
                elif i % 4 == 2:  # Bottom-right: place Red if available
                    r += 1
                    if red_used < R:
                        pieces.append(('R', r, c))
                        red_used += 1
                    else:
                        pieces.append(('B', r, c))
                        blue_used += 1
                else:  # Bottom-left: place Blue if available
                    c -= 1
                    if blue_used < B:
                        pieces.append(('B', r, c))
                        blue_used += 1
                    else:
                        pieces.append(('R', r, c))
                        red_used += 1
    
    return pieces

T = int(input())
for _ in range(T):
    R, B = map(int, input().split())
    result = solve(R, B)
    
    if result is None:
        print("No")
    else:
        print("Yes")
        for piece_type, r, c in result:
            print(f"{piece_type} {r} {c}")
