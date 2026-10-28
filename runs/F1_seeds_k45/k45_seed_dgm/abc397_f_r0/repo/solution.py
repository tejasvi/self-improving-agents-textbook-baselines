# Write your solution here. Read from stdin, write to stdout.

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    # Precompute distinct counts from the left
    # left_distinct[i] = count of distinct integers in a[0:i]
    left_distinct = [0] * (n + 1)
    left_set = set()
    for i in range(n):
        left_set.add(a[i])
        left_distinct[i + 1] = len(left_set)
    
    # Precompute distinct counts from the right
    # right_distinct[j] = count of distinct integers in a[j:n]
    right_distinct = [0] * (n + 1)
    right_set = set()
    for j in range(n - 1, -1, -1):
        right_set.add(a[j])
        right_distinct[j] = len(right_set)
    
    max_sum = 0
    
    # For each split position i (first cut), compute the best j for the second cut
    for i in range(n - 2):  # i can be 0 to n-3
        left_count = left_distinct[i + 1]
        
        # For this i, we need to try all j from i+1 to n-2
        # We can compute middle distinct counts incrementally
        middle_set = set()
        for j in range(i + 1, n - 1):  # j can be i+1 to n-2
            # Add a[j] to the middle set
            middle_set.add(a[j])
            middle_count = len(middle_set)
            
            # Count distinct in third subarray a[j+1:n]
            right_count = right_distinct[j + 1]
            
            total = left_count + middle_count + right_count
            max_sum = max(max_sum, total)
    
    print(max_sum)

solve()
