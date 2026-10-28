# Write your solution here. Read from stdin, write to stdout.

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    # Precompute left_distinct[i]: count of distinct elements in A[0:i+1]
    left_distinct = [0] * N
    seen = set()
    for i in range(N):
        seen.add(A[i])
        left_distinct[i] = len(seen)
    
    # Precompute right_distinct[j]: count of distinct elements in A[j:N]
    right_distinct = [0] * N
    seen = set()
    for j in range(N - 1, -1, -1):
        seen.add(A[j])
        right_distinct[j] = len(seen)
    
    max_sum = 0
    
    # Try all valid pairs (i, j) where 1 <= i < j <= N-1
    # In 0-indexed: 0 <= i < j <= N-2
    for i in range(N - 2):  # i can be from 0 to N-3
        # For this i, compute middle distinct counts for all j > i
        middle_set = set()
        for j in range(i + 1, N - 1):  # j can be from i+1 to N-2
            # Add A[j] to middle_set as we extend the middle range
            middle_set.add(A[j])
            middle_count = len(middle_set)
            
            # Count distinct in left part: A[0:i+1]
            left_count = left_distinct[i]
            
            # Count distinct in right part: A[j+1:N]
            right_count = right_distinct[j + 1]
            
            total = left_count + middle_count + right_count
            max_sum = max(max_sum, total)
    
    print(max_sum)

solve()
