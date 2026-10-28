def solve():
    H, W, N = map(int, input().split())
    
    # Store holed positions
    holes = set()
    for _ in range(N):
        a, b = map(int, input().split())
        holes.add((a, b))
    
    total = 0
    
    # For each possible top-left corner (i, j)
    for i in range(1, H + 1):
        for j in range(1, W + 1):
            # Find the maximum n such that the square is holeless
            # Maximum n is limited by grid boundaries
            max_n = min(H - i + 1, W - j + 1)
            
            # Find the maximum n such that no hole is in the square
            for hole_a, hole_b in holes:
                # If hole is in the region starting at (i, j)
                if i <= hole_a <= i + max_n - 1 and j <= hole_b <= j + max_n - 1:
                    # The hole limits n to be at most max(hole_a - i, hole_b - j)
                    max_n = min(max_n, max(hole_a - i, hole_b - j))
            
            # Add all valid square sizes starting at (i, j)
            total += max_n
    
    print(total)

solve()
