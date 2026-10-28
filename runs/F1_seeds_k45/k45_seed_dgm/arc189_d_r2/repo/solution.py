# Write your solution here. Read from stdin, write to stdout.

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    results = []
    
    # For each starting position K (0-indexed)
    for k in range(n):
        # Simulate the absorption process starting from position k
        # We'll keep track of which slimes are still in play
        valid = [True] * n
        valid[k] = False  # Takahashi is at position k, mark others as valid
        current_size = a[k]
        
        changed = True
        while changed:
            changed = False
            
            # Find the closest valid slime to the left
            left_pos = k - 1
            while left_pos >= 0 and not valid[left_pos]:
                left_pos -= 1
            
            # Find the closest valid slime to the right
            right_pos = k + 1
            while right_pos < n and not valid[right_pos]:
                right_pos += 1
            
            # Try absorbing left
            if left_pos >= 0 and a[left_pos] < current_size:
                current_size += a[left_pos]
                valid[left_pos] = False
                changed = True
                continue
            
            # Try absorbing right
            if right_pos < n and a[right_pos] < current_size:
                current_size += a[right_pos]
                valid[right_pos] = False
                changed = True
                continue
        
        results.append(current_size)
    
    print(' '.join(map(str, results)))

solve()
