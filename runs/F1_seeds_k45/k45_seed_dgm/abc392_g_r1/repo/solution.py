# Write your solution here. Read from stdin, write to stdout.

n = int(input())
s = list(map(int, input().split()))

# Convert to set for O(1) lookup
s_set = set(s)

count = 0

# For each pair (A, C) with A < C
# Check if B = (A + C) / 2 exists in S and A < B < C
for i in range(n):
    for j in range(i + 1, n):
        a = s[i]
        c = s[j]
        
        # Ensure a < c
        if a > c:
            a, c = c, a
        
        # Check if (a + c) is even so that B is an integer
        if (a + c) % 2 == 0:
            b = (a + c) // 2
            # Check if B exists in the set and satisfies a < b < c
            if b in s_set and a < b < c:
                count += 1

print(count)
