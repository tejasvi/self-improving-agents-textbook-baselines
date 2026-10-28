# Write your solution here. Read from stdin, write to stdout.

def solve():
    H, W, N = map(int, input().split())
    
    # Read holed squares
    holed = set()
    for _ in range(N):
        a, b = map(int, input().split())
        holed.add((a, b))
    
    total = 0
    
    # For each possible top-left corner (i, j)
    for i in range(1, H + 1):
        for j in range(1, W + 1):
            # Find maximum holeless square size starting at (i, j)
            # The maximum possible size is limited by the grid boundaries
            max_possible = min(H - i + 1, W - j + 1)
            
            # Check sizes from 1 to max_possible
            # We want to find the largest n such that the n×n square is holeless
            max_holeless = 0
            
            for n in range(1, max_possible + 1):
                # Check if the n×n square starting at (i, j) contains any holes
                # The square covers (i, j) to (i + n - 1, j + n - 1)
                
                # Check if any holed square is in this region
                has_hole = False
                for hole_i, hole_j in holed:
                    if i <= hole_i <= i + n - 1 and j <= hole_j <= j + n - 1:
                        has_hole = True
                        break
                
                if not has_hole:
                    max_holeless = n
                else:
                    # Once we find a hole, all larger squares will also contain this hole
                    break
            
            # Add all valid square sizes at this position
            total += max_holeless
    
    print(total)

solve()
