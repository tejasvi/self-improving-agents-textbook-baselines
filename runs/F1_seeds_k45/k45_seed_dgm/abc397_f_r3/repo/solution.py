# Write your solution here. Read from stdin, write to stdout.

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    # Precompute distinct count for all prefixes
    # distinct_left[i] = count of distinct integers in a[0:i]
    distinct_left = [0] * (n + 1)
    seen_left = set()
    for i in range(n):
        seen_left.add(a[i])
        distinct_left[i + 1] = len(seen_left)
    
    # Precompute distinct count for all suffixes
    # distinct_right[i] = count of distinct integers in a[i:n]
    distinct_right = [0] * (n + 1)
    seen_right = set()
    for i in range(n - 1, -1, -1):
        seen_right.add(a[i])
        distinct_right[i] = len(seen_right)
    
    max_sum = 0
    
    # Try all valid pairs (i, j) where 1 <= i < j <= n-1
    # In 0-indexed: 0 <= i < j <= n-2
    for i in range(n - 2):  # i can be 0 to n-3
        # For each i, compute middle counts incrementally as j increases
        middle_seen = set()
        for j in range(i + 1, n - 1):  # j can be i+1 to n-2
            # First subarray: a[0:i+1]
            left_count = distinct_left[i + 1]
            
            # Third subarray: a[j+1:n]
            right_count = distinct_right[j + 1]
            
            # Second subarray: a[i+1:j+1]
            # Build incrementally
            if j == i + 1:
                middle_seen = {a[j]}
            else:
                middle_seen.add(a[j])
            middle_count = len(middle_seen)
            
            total = left_count + middle_count + right_count
            max_sum = max(max_sum, total)
    
    print(max_sum)

solve()
