def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    results = []
    
    for k in range(N):
        # Start from position k with size A[k]
        current_size = A[k]
        
        # Use a different approach: expand left and right
        left = k - 1
        right = k + 1
        
        while True:
            absorbed_any = False
            
            # Try to absorb from left
            while left >= 0 and A[left] < current_size:
                current_size += A[left]
                left -= 1
                absorbed_any = True
            
            # Try to absorb from right
            while right < N and A[right] < current_size:
                current_size += A[right]
                right += 1
                absorbed_any = True
            
            if not absorbed_any:
                break
        
        results.append(current_size)
    
    print(' '.join(map(str, results)))

solve()
