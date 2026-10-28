def solve(R, B):
    total = R + B
    
    # Case 1: Only blue pieces (B > 0, R = 0)
    if R == 0:
        if B < 2:
            return None
        if B % 2 == 1:  # Odd number of diagonal moves can't form cycle
            return None
        
        # Arrange blues in a pattern that forms a cycle
        # Simple: arrange in a 2xB/2 rectangle of blues moving diagonally
        pieces = []
        r = 1
        for i in range(B):
            c = 1 + i
            pieces.append(('B', r, c))
            if i == B // 2 - 1:
                r = 2
        return pieces
    
    # Case 2: Only red pieces (R > 0, B = 0)
    if B == 0:
        if R < 2:
            return None
        
        # Form a simple rectangular cycle with red pieces
        # Make a 2x(R/2) or just use simple path
        pieces = []
        
        if R == 2:
            pieces = [
                ('R', 1, 1),
                ('R', 1, 2),
            ]
        elif R == 3:
            pieces = [
                ('R', 1, 1),
                ('R', 1, 2),
                ('R', 2, 2),
            ]
        elif R == 4:
            pieces = [
                ('R', 1, 1),
                ('R', 1, 2),
                ('R', 2, 2),
                ('R', 2, 1),
            ]
        else:
            # General rectangular pattern
            cols = (R + 1) // 2
            for i in range(R):
                r = 1 + (i % 2)
                c = 1 + (i // 2)
                pieces.append(('R', r, c))
        
        return pieces
    
    # Case 3: Both R > 0 and B > 0
    # Special case: R = 1, B = 1 is impossible
    if R == 1 and B == 1:
        return None
    
    # For R >= 1, B >= 1, we can try to construct a solution
    # Strategy: place pieces in a pattern that works
    
    # Try a general construction:
    # We can arrange them as follows
    pieces = []
    
    # One heuristic: if both exist, try to build a path
    # Red pieces form a base path, blues augment it
    
    if R == 1:
        # R = 1, B >= 2
        # Place blue-red-blue pattern
        if B < 2:
            return None
        if B % 2 == 0:
            # Even blues: B, R, B, B, B, ...
            # Actually let's use: all blues in cycle, then insert red
            pieces = []
            for i in range(B):
                c = 1 + i
                r = 1 if i % 2 == 0 else 2
                pieces.append(('B', r, c))
            
            # Now we need to insert 1 red
            # This is tricky - we need to break the blue cycle and insert red
            # Let's try a different approach
            
            # Place reds and blues alternately
            # Actually, simpler: use a corner pattern
            pieces = [
                ('B', 1, 1),
                ('B', 2, 2),
            ]
            for i in range(2, B):
                if i % 2 == 0:
                    pieces.append(('B', 1, 1 + i))
                else:
                    pieces.append(('B', 2, 1 + i))
            pieces.append(('R', 1, 2))
            return pieces
        else:
            # Odd blues with 1 red
            return None
    
    # R >= 2, B >= 1
    # General construction
    pieces = []
    
    # Place all reds first in a path
    for i in range(R):
        r = 1 + (i % 2)
        c = 1 + (i // 2)
        pieces.append(('R', r, c))
    
    # Then place all blues
    for i in range(B):
        r = 3 + (i % 2)
        c = 1 + (i // 2)
        pieces.append(('B', r, c))
    
    return pieces

def format_output(pieces):
    if pieces is None:
        return "No"
    
    result = ["Yes"]
    for piece_type, r, c in pieces:
        result.append(f"{piece_type} {r} {c}")
    
    return "\n".join(result)

def main():
    T = int(input())
    for _ in range(T):
        R, B = map(int, input().split())
        pieces = solve(R, B)
        print(format_output(pieces))

if __name__ == "__main__":
    main()
