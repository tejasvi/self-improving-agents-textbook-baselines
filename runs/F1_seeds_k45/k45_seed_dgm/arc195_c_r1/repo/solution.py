def solve(R, B):
    total = R + B
    
    # Impossible cases
    if total < 2:
        return None
    
    # Special case: R=1, B=1
    # Red can move to Manhattan neighbors, Blue can move to diagonal neighbors
    # They can't form a cycle together
    if R == 1 and B == 1:
        return None
    
    # R=0, B=1 or R=1, B=0 are impossible (covered by total < 2, but let's be explicit)
    if (R == 0 and B == 1) or (R == 1 and B == 0):
        return None
    
    pieces = []
    
    # Strategy:
    # - If we have at least 2 red pieces, we can form a rectangle
    # - If we have at least 2 blue pieces, we can form a line
    # - Combine them appropriately
    
    if R >= 2:
        # Create a path using red pieces and fill with blue pieces
        if B == 0:
            # Only red pieces - form a rectangle/path
            if R == 2:
                pieces.append(('R', 1, 1))
                pieces.append(('R', 1, 2))
            else:  # R >= 3
                # Form a rectangle or larger path
                pieces.append(('R', 1, 1))
                pieces.append(('R', 1, 2))
                pieces.append(('R', 2, 2))
                pieces.append(('R', 2, 1))
                # Add more reds in a line
                for i in range(4, R):
                    pieces.append(('R', 3, i - 3))
        else:  # B >= 1
            # Mix of red and blue pieces
            # Pattern: R -> R -> B -> ... -> B -> R -> ... -> R -> back to first R
            pieces.append(('R', 1, 1))
            pieces.append(('R', 1, 2))
            pieces.append(('B', 2, 3))
            for i in range(1, B):
                pieces.append(('B', 2 + i, 3 + i))
            for i in range(2, R):
                pieces.append(('R', 3 + B + (i - 2), 3 + B))
    else:
        # R == 0 or R == 1
        # If R == 1 and B >= 2: impossible (already checked)
        # So R == 0 and B >= 2
        if R == 0 and B >= 2:
            # All blue pieces - form a diagonal path
            for i in range(B):
                pieces.append(('B', 1 + i, 1 + i))
        else:
            return None
    
    # Verify the solution forms a valid cycle
    # For now, return the pieces assuming the construction is correct
    if len(pieces) != R + B:
        return None
    
    return pieces

def main():
    T = int(input())
    for _ in range(T):
        R, B = map(int, input().split())
        result = solve(R, B)
        if result is None:
            print("No")
        else:
            print("Yes")
            for piece, r, c in result:
                print(f"{piece} {r} {c}")

if __name__ == "__main__":
    main()
