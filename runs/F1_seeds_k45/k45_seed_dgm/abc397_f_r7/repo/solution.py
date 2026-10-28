def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    # Precompute prefix distinct counts
    # prefix_distinct[i] = number of distinct elements in A[0:i+1]
    prefix_distinct = [0] * N
    seen = set()
    for i in range(N):
        seen.add(A[i])
        prefix_distinct[i] = len(seen)
    
    # Precompute suffix distinct counts
    # suffix_distinct[i] = number of distinct elements in A[i:N]
    suffix_distinct = [0] * N
    seen = set()
    for i in range(N-1, -1, -1):
        seen.add(A[i])
        suffix_distinct[i] = len(seen)
    
    max_sum = 0
    
    # Try all pairs (i, j) where 0 <= i < j < N-1 (in 0-indexed)
    # Subarray 1: A[0:i+1]
    # Subarray 2: A[i+1:j+1]
    # Subarray 3: A[j+1:N]
    
    for i in range(N-2):  # i can be 0 to N-3
        # For fixed i, iterate j from i+1 to N-2
        # and maintain a set of elements in A[i+1:j+1] incrementally
        seen_middle = set()
        for j in range(i+1, N-1):  # j can be i+1 to N-2
            # Add A[j] to the middle subarray
            seen_middle.add(A[j])
            
            # Count distinct in first subarray A[0:i+1]
            count1 = prefix_distinct[i]
            
            # Count distinct in third subarray A[j+1:N]
            count3 = suffix_distinct[j+1]
            
            # Count distinct in middle subarray A[i+1:j+1]
            count2 = len(seen_middle)
            
            total = count1 + count2 + count3
            max_sum = max(max_sum, total)
    
    print(max_sum)

solve()
