n = int(input())
s = list(map(int, input().split()))

# Convert to set for O(1) lookup
s_set = set(s)

count = 0

# For each potential middle element B
for b in s:
    # Try all possible differences d
    d = 1
    while b - d > 0 and b + d <= max(s):
        a = b - d
        c = b + d
        
        # Check if both a and c are in the set
        if a in s_set and c in s_set:
            count += 1
        
        d += 1

print(count)
