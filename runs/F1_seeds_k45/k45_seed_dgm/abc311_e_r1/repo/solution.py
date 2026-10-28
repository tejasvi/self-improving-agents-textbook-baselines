def solve():
    H, W, N = map(int, input().split())
    
    holes = set()
    for _ in range(N):
        a, b = map(int, input().split())
        holes.add((a, b))
    
    # dp[i][j] = maximum size of holeless square with top-left at (i, j)
    dp = [[0] * (W + 1) for _ in range(H + 1)]
    
    total = 0
    
    # Process from bottom-right to top-left
    for i in range(H, 0, -1):
        for j in range(W, 0, -1):
            if (i, j) in holes:
                dp[i][j] = 0
            else:
                # Maximum possible size limited by boundaries
                max_possible = min(H - i + 1, W - j + 1)
                
                # The size can be at most 1 + min of sizes from adjacent cells
                # But we need to be careful about the recursive structure
                if i == H or j == W:
                    # At boundaries, we can have size 1
                    size = 1
                else:
                    # Size is limited by cells below, right, and diagonal
                    size = min(dp[i+1][j], dp[i][j+1], dp[i+1][j+1]) + 1
                    size = min(size, max_possible)
                
                dp[i][j] = size
                total += size
    
    print(total)

solve()
