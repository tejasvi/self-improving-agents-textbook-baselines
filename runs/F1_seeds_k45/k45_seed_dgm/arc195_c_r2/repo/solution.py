# Write your solution here. Read from stdin, write to stdout.

def solve(R, B):
    total = R + B
    
    # Special case: impossible cases
    # If only 1 red and 1 blue: they can't form a cycle (different movement types)
    if R == 1 and B == 1:
        return None
    
    # If only blues with count < 4: impossible
    if R == 0 and B < 4:
        return None
    
    # If only reds with count < 4: impossible
    if B == 0 and R < 4:
        return None
    
    # If only blues and count >= 4:
    # Blues move diagonally, we can form a cycle
    if R == 0 and B >= 4:
        # Form a rectangle cycle with blue pieces
        pieces = []
        positions = [(1, 1), (1, 3), (3, 3), (3, 1)]
        for i in range(B):
            pos = positions[i % 4]
            pieces.append(('B', pos[0], pos[1]))
        return pieces
    
    # If only reds and count >= 4:
    if B == 0 and R >= 4:
        # Form a 2x2 square
        pieces = []
        positions = [(1, 1), (1, 2), (2, 2), (2, 1)]
        for i in range(R):
            pos = positions[i % 4]
            pieces.append(('R', pos[0], pos[1]))
        return pieces
    
    # If we have both reds and blues
    # For R >= 2 and B >= 2, we can construct
    if R >= 2 and B >= 2:
        pieces = []
        
        # Use a clever pattern that works
        # Place them alternating in a diagonal-like pattern
        # Red (1,1) -> Blue (2,2) -> Red (2,3) -> Blue (3,4) -> ...
        
        # Actually simpler: create an extended grid pattern
        r, c = 1, 1
        for i in range(total):
            if i < R:
                # Place reds first
                pieces.append(('R', r, c))
            else:
                # Place blues after reds
                pieces.append(('B', r, c))
            
            # Move pattern to create valid moves
            if i % 2 == 0:
                c += 1  # Move right (works for red)
            else:
                r += 1  # Move down (works for red)
        
        return pieces
    
    # For R=1, B >= 2, or R >= 2, B=1 - more complex
    # Let's check if B >= 3 and R == 1
    if R == 1 and B >= 3:
        # Red at (1,2), Blue pieces around it
        pieces = []
        pieces.append(('R', 1, 2))
        # Blue at (2,1), (2,3), (3,2)
        positions = [(2, 1), (2, 3), (3, 2)]
        for i in range(B - 1):
            pos = positions[i % len(positions)]
            pieces.append(('B', pos[0], pos[1]))
        return pieces if len(pieces) == total else None
    
    # For R >= 3 and B == 1
    if R >= 3 and B == 1:
        # Create a pattern where blue can fit
        pieces = []
        pieces.append(('R', 1, 1))
        pieces.append(('B', 2, 2))
        pieces.append(('R', 3, 1))
        for i in range(3, R):
            pieces.append(('R', 1, 1 + i))
        return pieces if len(pieces) == total else None
    
    return None


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
