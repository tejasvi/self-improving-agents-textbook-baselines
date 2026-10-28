# Write your solution here. Read from stdin, write to stdout.

def solve():
    H, W, N = map(int, input().split())
    
    # Store holed squares in a set for O(1) lookup
    holed = set()
    for _ in range(N):
        a, b = map(int, input().split())
        holed.add((a, b))
    
    # If there are no holes, use formula
    if N == 0:
        # For each size n, count how many positions can fit an n×n square
        # = (H - n + 1) * (W - n + 1) if n <= min(H, W)
        total = 0
        max_n = min(H, W)
        for n in range(1, max_n + 1):
            total += (H - n + 1) * (W - n + 1)
        print(total)
        return
    
    count = 0
    
    # For each position, compute the maximum size of holeless square starting there
    max_size = [[0] * (W + 1) for _ in range(H + 1)]
    
    # Process from bottom-right to top-left
    for i in range(H, 0, -1):
        for j in range(W, 0, -1):
            if (i, j) in holed:
                max_size[i][j] = 0
            else:
                # Compute max size starting at (i, j)
                # Check increasing sizes until we hit a hole or boundary
                max_possible = min(H - i + 1, W - j + 1)
                
                # If we know that no holes exist in all positions, we can use previous info
                # But we need to be careful - we check incrementally
                m = 0
                for n in range(1, max_possible + 1):
                    has_hole = False
                    
                    # Check if this n×n square is holeless
                    if n == 1:
                        # Already checked above - (i,j) is not holed
                        has_hole = False
                    else:
                        # Check the new row and column
                        for k in range(j, j + n):
                            if (i + n - 1, k) in holed:
                                has_hole = True
                                break
                        
                        if not has_hole:
                            for k in range(i, i + n - 1):
                                if (k, j + n - 1) in holed:
                                    has_hole = True
                                    break
                    
                    if not has_hole:
                        m = n
                    else:
                        break
                
                max_size[i][j] = m
                count += m
    
    print(count)

solve()
