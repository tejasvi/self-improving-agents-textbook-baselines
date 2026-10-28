def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    results = []
    
    # For each starting position K (0-indexed)
    for k in range(N):
        # Simulate the absorption process
        slimes = list(A)  # Work with a copy of the array
        
        current_idx = k  # Index in the slimes list
        current_size = slimes[k]
        
        # Keep absorbing while possible
        changed = True
        while changed:
            changed = False
            
            # Try to absorb left
            while current_idx > 0 and slimes[current_idx - 1] < current_size:
                current_size += slimes[current_idx - 1]
                slimes.pop(current_idx - 1)
                current_idx -= 1
                changed = True
            
            # Try to absorb right
            while current_idx < len(slimes) - 1 and slimes[current_idx + 1] < current_size:
                current_size += slimes[current_idx + 1]
                slimes.pop(current_idx + 1)
                changed = True
        
        results.append(current_size)
    
    print(' '.join(map(str, results)))

solve()
