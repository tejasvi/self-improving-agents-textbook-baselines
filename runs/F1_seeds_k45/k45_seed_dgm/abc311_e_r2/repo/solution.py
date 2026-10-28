def solve():
    H, W, N = map(int, input().split())
    
    holes = set()
    for _ in range(N):
        a, b = map(int, input().split())
        holes.add((a, b))
    
    count = 0
    
    # For each starting position (i, j)
    for i in range(1, H + 1):
        for j in range(1, W + 1):
            # Find the maximum size n for this starting position
            # Maximum possible size based on grid boundaries
            max_n = min(H - i + 1, W - j + 1)
            
            # Check each size from 1 to max_n
            for n in range(1, max_n + 1):
                # Check if the square (i, j) to (i+n-1, j+n-1) is holeless
                is_holeless = True
                
                # Check if any hole is in this square
                for hole_i, hole_j in holes:
                    if i <= hole_i <= i + n - 1 and j <= hole_j <= j + n - 1:
                        is_holeless = False
                        break
                
                if is_holeless:
                    count += 1
                else:
                    # If we found a hole, no larger square from this position will be holeless
                    break
    
    print(count)

solve()
