def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    # Precompute distinct counts for all prefixes
    # prefix_distinct[i] = count of distinct elements in a[0:i]
    prefix_distinct = [0] * (n + 1)
    prefix_set = set()
    for i in range(n):
        prefix_set.add(a[i])
        prefix_distinct[i + 1] = len(prefix_set)
    
    # Precompute distinct counts for all suffixes
    # suffix_distinct[i] = count of distinct elements in a[i:n]
    suffix_distinct = [0] * (n + 1)
    suffix_set = set()
    for i in range(n - 1, -1, -1):
        suffix_set.add(a[i])
        suffix_distinct[i] = len(suffix_set)
    
    max_sum = 0
    
    # Try all possible split positions i and j
    # i is the end of first subarray (exclusive), j is the end of second subarray (exclusive)
    for i in range(1, n - 1):  # i from 1 to n-2 (ensures first subarray has at least 1 element)
        left_distinct = prefix_distinct[i]
        
        # For this i, try all j values and compute middle part efficiently
        middle_set = set()
        for j in range(i + 1, n):  # j from i+1 to n-1 (ensures second subarray has at least 1 element)
            # Build middle set incrementally as we extend j
            middle_set.add(a[j - 1])
            middle_distinct = len(middle_set)
            
            # Right part: a[j:n]
            right_distinct = suffix_distinct[j]
            
            current_sum = left_distinct + middle_distinct + right_distinct
            max_sum = max(max_sum, current_sum)
    
    print(max_sum)

solve()
