def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    # Compute prefix counts: prefix[i] = number of distinct elements in a[0:i]
    prefix = [0] * (n + 1)
    seen = set()
    for i in range(n):
        seen.add(a[i])
        prefix[i + 1] = len(seen)
    
    # Compute suffix counts: suffix[i] = number of distinct elements in a[i:n]
    suffix = [0] * (n + 1)
    seen = set()
    for i in range(n - 1, -1, -1):
        seen.add(a[i])
        suffix[i] = len(seen)
    
    max_sum = 0
    
    # Try all valid pairs (i, j) where 1 <= i < j <= n-1
    # In 0-indexed terms: 0 <= i < j <= n-2 (since we need i < j and j < n)
    # But we need to be careful with indexing
    # i is the split point after position i (1-indexed), so in 0-indexed it's after a[i]
    # j is the split point after position j (1-indexed), so in 0-indexed it's after a[j]
    
    for i in range(1, n - 1):  # i from 1 to n-2 (inclusive)
        for j in range(i + 1, n):  # j from i+1 to n-1 (inclusive)
            # Subarray 1: a[0:i] (first i elements)
            distinct1 = prefix[i]
            
            # Subarray 3: a[j:n] (from position j to end)
            distinct3 = suffix[j]
            
            # Subarray 2: a[i:j] (from position i to j-1)
            seen = set()
            for k in range(i, j):
                seen.add(a[k])
            distinct2 = len(seen)
            
            total = distinct1 + distinct2 + distinct3
            max_sum = max(max_sum, total)
    
    print(max_sum)

solve()
