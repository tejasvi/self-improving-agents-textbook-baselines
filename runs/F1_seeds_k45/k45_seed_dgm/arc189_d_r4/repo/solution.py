def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    results = []
    
    # For each starting position K
    for K in range(N):
        size = A[K]
        
        # Find all slimes we can absorb
        # A slime is absorbable if there's a path to it through strictly smaller slimes
        left = K - 1
        right = K + 1
        
        # Expand left while we can absorb
        while left >= 0 and A[left] < size:
            size += A[left]
            left -= 1
        
        # Expand right while we can absorb
        while right < N and A[right] < size:
            size += A[right]
            right += 1
        
        # Now we might be able to go back left or right if our size increased
        # Keep expanding until we can't
        changed = True
        while changed:
            changed = False
            
            # Try expanding left
            while left >= 0 and A[left] < size:
                size += A[left]
                left -= 1
                changed = True
            
            # Try expanding right
            while right < N and A[right] < size:
                size += A[right]
                right += 1
                changed = True
        
        results.append(size)
    
    print(' '.join(map(str, results)))

solve()
