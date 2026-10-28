# Write your solution here. Read from stdin, write to stdout.

def solve():
    H, W, N = map(int, input().split())
    
    # Store all holes
    holes = []
    
    for _ in range(N):
        a, b = map(int, input().split())
        holes.append((a, b))
    
    # If there are no holes, we can use a formula
    if N == 0:
        # For an H×W grid with no holes
        # Count of all squares of size n is (H-n+1) * (W-n+1)
        # Total = sum of (H-n+1) * (W-n+1) for n from 1 to min(H,W)
        total = 0
        for n in range(1, min(H, W) + 1):
            total += (H - n + 1) * (W - n + 1)
        print(total)
        return
    
    # For each possible top-left corner (i, j), find max square size
    count = 0
    
    for i in range(1, H + 1):
        for j in range(1, W + 1):
            # Find the maximum n such that the n×n square starting at (i,j) is holeless
            max_n = min(H - i + 1, W - j + 1)
            
            # Check each size from 1 to max_n
            for n in range(1, max_n + 1):
                # Check if this n×n square contains any holes
                is_holeless = True
                for a, b in holes:
                    # Check if hole (a, b) is within the n×n square starting at (i, j)
                    if i <= a <= i + n - 1 and j <= b <= j + n - 1:
                        is_holeless = False
                        break
                
                if is_holeless:
                    count += 1
                else:
                    # If we found a hole, no larger square will work
                    break
    
    print(count)

solve()
