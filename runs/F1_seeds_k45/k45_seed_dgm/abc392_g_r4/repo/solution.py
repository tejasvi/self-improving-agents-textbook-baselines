n = int(input())
s = list(map(int, input().split()))

# Convert to set for O(1) lookup
s_set = set(s)

count = 0

# Iterate through all pairs (A, C) where A < C
for i in range(n):
    for j in range(i + 1, n):
        a = s[i]
        c = s[j]
        
        # Make sure a < c
        if a > c:
            a, c = c, a
        
        # Check if B = (A + C) / 2 exists in the set
        if (a + c) % 2 == 0:  # B must be an integer
            b = (a + c) // 2
            if b in s_set and a < b < c:
                count += 1

print(count)
