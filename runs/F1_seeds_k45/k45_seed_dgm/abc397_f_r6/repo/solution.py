def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    # Precompute prefix distinct counts
    # prefix[i] = number of distinct elements in a[0:i]
    prefix = [0] * (n + 1)
    prefix_set = set()
    for i in range(n):
        prefix_set.add(a[i])
        prefix[i + 1] = len(prefix_set)
    
    # Precompute suffix distinct counts
    # suffix[i] = number of distinct elements in a[i:n]
    suffix = [0] * (n + 1)
    suffix_set = set()
    for i in range(n - 1, -1, -1):
        suffix_set.add(a[i])
        suffix[i] = len(suffix_set)
    
    max_sum = 0
    
    # Try all valid (i, j) pairs
    # i ranges from 1 to n-2 (inclusive), so first subarray has at least 1 element
    # j ranges from i+1 to n-1 (inclusive), so middle and last subarrays have at least 1 element
    for i in range(1, n - 1):
        middle_set = set()
        # j ranges from i+1 to n-1
        for j in range(i + 1, n):
            # Add elements from a[i:j] to the middle set
            middle_set.add(a[j - 1])
            
            prefix_count = prefix[i]  # distinct in a[0:i]
            middle_count = len(middle_set)  # distinct in a[i:j]
            suffix_count = suffix[j]  # distinct in a[j:n]
            
            current_sum = prefix_count + middle_count + suffix_count
            max_sum = max(max_sum, current_sum)
    
    print(max_sum)

solve()
