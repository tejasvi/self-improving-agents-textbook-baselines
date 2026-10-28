# Write your solution here. Read from stdin, write to stdout.

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    # Precompute count of distinct elements in prefixes
    # left_distinct[i] = count of distinct in a[0:i+1]
    left_distinct = [0] * n
    seen = set()
    for i in range(n):
        seen.add(a[i])
        left_distinct[i] = len(seen)
    
    # Precompute count of distinct elements in suffixes
    # right_distinct[i] = count of distinct in a[i:n]
    right_distinct = [0] * n
    seen = set()
    for i in range(n - 1, -1, -1):
        seen.add(a[i])
        right_distinct[i] = len(seen)
    
    max_sum = 0
    
    # Try all pairs (i, j) where 0 <= i < j <= n-2
    # This means left part is a[0:i+1], middle is a[i+1:j+1], right is a[j+1:n]
    for i in range(n - 2):  # i from 0 to n-3
        seen_middle = set()
        for j in range(i + 1, n - 1):  # j from i+1 to n-2
            # Add a[j] to middle part
            seen_middle.add(a[j])
            
            total = left_distinct[i] + len(seen_middle) + right_distinct[j + 1]
            if total > max_sum:
                max_sum = total
    
    print(max_sum)

solve()
