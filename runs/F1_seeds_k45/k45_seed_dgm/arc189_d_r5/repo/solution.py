# Write your solution here. Read from stdin, write to stdout.

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    results = []
    
    # For each starting position K (0-indexed)
    for k in range(n):
        # Create a list of slimes with their current sizes and original indices
        # We'll track the actual slimes and Takahashi's position
        slimes = list(a)  # Copy of all slime sizes
        takahashi_pos = k
        takahashi_size = slimes[takahashi_pos]
        
        # Keep absorbing until no more moves are possible
        changed = True
        while changed:
            changed = False
            
            # Try to absorb left neighbor
            if takahashi_pos > 0 and slimes[takahashi_pos - 1] < takahashi_size:
                takahashi_size += slimes[takahashi_pos - 1]
                slimes.pop(takahashi_pos - 1)
                takahashi_pos -= 1
                changed = True
            # Try to absorb right neighbor
            elif takahashi_pos < len(slimes) - 1 and slimes[takahashi_pos + 1] < takahashi_size:
                takahashi_size += slimes[takahashi_pos + 1]
                slimes.pop(takahashi_pos + 1)
                changed = True
        
        results.append(takahashi_size)
    
    print(' '.join(map(str, results)))

solve()
