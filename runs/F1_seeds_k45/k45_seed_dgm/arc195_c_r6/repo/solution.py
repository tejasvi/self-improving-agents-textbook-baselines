# Write your solution here. Read from stdin, write to stdout.

def solve():
    T = int(input())
    
    for _ in range(T):
        R, B = map(int, input().split())
        total = R + B
        
        # Edge cases where no solution exists
        # With only 1 red piece and no blue pieces - can't form a cycle
        if R == 1 and B == 0:
            print("No")
            continue
        
        # With only 1 blue piece and no red pieces - can't form a cycle
        if R == 0 and B == 1:
            print("No")
            continue
        
        # With 1 red and 1 blue - red can move to blue, but blue (diagonal) can't move back to red
        # Actually, let's check: Red at (1,1), Blue at (1,2). Red can move right to (1,2).
        # Blue needs to move diagonally back to (1,1). From (1,2), blue can go to (0,1), (0,3), (2,1), (2,3).
        # None of these is (1,1). So this is impossible.
        if R == 1 and B == 1:
            print("No")
            continue
        
        # With only blue pieces and odd number of them, it's impossible
        # This is because blue moves diagonally, which changes both row and column parity
        # For a cycle to exist with only blue pieces, they must form a proper cycle
        # A blue piece at (r, c) can only reach positions where (r+c) has opposite parity
        # So they need to alternate between two parity classes
        if R == 0 and B % 2 == 1:
            print("No")
            continue
        
        # If we reach here, a solution should exist
        print("Yes")
        
        # Strategy: Use a construction that works
        # Key insight: We can place pieces in a rectangle pattern
        
        if B == 0:
            # Only red pieces (R >= 2)
            # Create a rectangular cycle
            # Place them in a 2 x ceil(R/2) grid in a zigzag
            positions = []
            count = 0
            
            # Go right in row 1, then left in row 2
            c = 1
            while count < R:
                positions.append((1, c, 'R'))
                count += 1
                c += 1
            
            c -= 1  # Go back to last column used
            while count < R:
                positions.append((2, c, 'R'))
                count += 1
                c -= 1
            
            for r, c, color in positions:
                print(f"{color} {r} {c}")
        
        elif R == 0:
            # Only blue pieces (B >= 2 and even)
            # Blue moves diagonally
            # Place in alternating checkerboard pattern
            # B at (1,1), then (2,2), then (1,3), then (2,4), etc.
            positions = []
            
            for i in range(B):
                if i % 2 == 0:
                    r = 1
                    c = 1 + i
                else:
                    r = 2
                    c = 1 + i
                positions.append((r, c, 'B'))
            
            for r, c, color in positions:
                print(f"{color} {r} {c}")
        
        else:
            # Both red and blue pieces (R >= 2 or B >= 2, and not the invalid cases)
            # Use a careful arrangement
            
            # One approach: arrange them in a pattern where they connect properly
            # For example, we can use a spiral or rectangular pattern
            
            positions = []
            
            # Strategy: Create a 2-row pattern where pieces alternate cleverly
            # Row 1: pieces moving right (and diagonally for blue)
            # Row 2: pieces moving left (and diagonally for blue)
            
            # Better strategy: interleave red and blue optimally
            # For simplicity, group them: first all of one type, then the other
            
            # Actually, let's use a 2x(R+B) grid pattern
            # Where we place pieces and ensure connectivity
            
            # Simple construction that should work:
            # Place pieces in a rectangle, carefully
            
            if R >= 1 and B >= 1:
                # We have both types
                # Strategy: place them in a pattern on a 2-row grid
                
                positions = []
                col = 1
                
                # Place some pieces strategically
                # Row 1 pattern: R, R, ..., then B, B, ...
                # Row 2 pattern: reversed
                
                for _ in range(R):
                    positions.append((1, col, 'R'))
                    col += 1
                
                for _ in range(B):
                    positions.append((1, col, 'B'))
                    col += 1
                
                # Now row 2, reversed
                col -= 1
                for _ in range(B):
                    positions.append((2, col, 'B'))
                    col -= 1
                
                for _ in range(R):
                    positions.append((2, col, 'R'))
                    col -= 1
                
                for r, c, color in positions:
                    print(f"{color} {r} {c}")

solve()
