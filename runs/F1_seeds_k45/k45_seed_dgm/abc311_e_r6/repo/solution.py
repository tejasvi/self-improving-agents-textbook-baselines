#!/usr/bin/env python3

def solve():
    H, W, N = map(int, input().split())
    
    holes = set()
    for _ in range(N):
        a, b = map(int, input().split())
        holes.add((a, b))
    
    total = 0
    
    # For each starting position (i, j)
    for i in range(1, H + 1):
        for j in range(1, W + 1):
            # Find the maximum size of holeless square starting at (i, j)
            max_size = min(H - i + 1, W - j + 1)
            
            # Check each size from 1 to max_size
            for n in range(1, max_size + 1):
                # Check if n×n square starting at (i, j) is holeless
                # Square spans from (i, j) to (i+n-1, j+n-1)
                is_holeless = True
                
                for a, b in holes:
                    if i <= a <= i + n - 1 and j <= b <= j + n - 1:
                        is_holeless = False
                        break
                
                if is_holeless:
                    total += 1
                else:
                    # If we found a hole, larger sizes will also contain this hole
                    break
    
    print(total)

solve()
