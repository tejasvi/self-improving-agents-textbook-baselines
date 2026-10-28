#!/usr/bin/env python3

n = int(input())
s = list(map(int, input().split()))

# Convert to set for O(1) lookup
s_set = set(s)

# Sort for easier iteration
s_sorted = sorted(s)

count = 0

# For each element as the middle element B
for i in range(n):
    b = s_sorted[i]
    
    # For each element smaller than B as A
    for j in range(i):
        a = s_sorted[j]
        
        # Calculate what C should be: A + C = 2*B => C = 2*B - A
        c = 2 * b - a
        
        # Check if C exists in the set and C > B
        if c in s_set and c > b:
            count += 1

print(count)
