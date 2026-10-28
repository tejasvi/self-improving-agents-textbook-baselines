# Write your solution here. Read from stdin, write to stdout.

def solve():
    # Read input
    H, W, N = map(int, input().split())
    
    # Store holed squares in a set for O(1) lookup
    holed = set()
    for _ in range(N):
        a, b = map(int, input().split())
        holed.add((a, b))
    
    count = 0
    
    # If there are no holes, use the formula: sum of all possible square sizes
    if N == 0:
        # For an H×W grid, the number of n×n squares is (H-n+1)*(W-n+1) for each n
        # Total = sum over n from 1 to min(H,W) of (H-n+1)*(W-n+1)
        for n in range(1, min(H, W) + 1):
            count += (H - n + 1) * (W - n + 1)
        print(count)
        return
    
    # For each possible top-left corner (i, j)
    for i in range(1, H + 1):
        for j in range(1, W + 1):
            # For each possible size n
            # Maximum possible size is limited by grid boundaries
            max_size = min(H - i + 1, W - j + 1)
            
            for n in range(1, max_size + 1):
                # Check if n×n square starting at (i, j) is holeless
                is_holeless = True
                
                # Only check the "new" cells added when expanding from (n-1)×(n-1) to n×n
                # These are the cells in row (i+n-1) and column (j+n-1)
                
                # Check the rightmost column: (i+k, j+n-1) for k in [0, n-1]
                for k in range(n):
                    if (i + k, j + n - 1) in holed:
                        is_holeless = False
                        break
                
                # Check the bottom row: (i+n-1, j+l) for l in [0, n-2]
                if is_holeless:
                    for l in range(n - 1):
                        if (i + n - 1, j + l) in holed:
                            is_holeless = False
                            break
                
                if is_holeless:
                    count += 1
                else:
                    # If we found a hole, all larger squares will also contain it
                    break
    
    print(count)

solve()
