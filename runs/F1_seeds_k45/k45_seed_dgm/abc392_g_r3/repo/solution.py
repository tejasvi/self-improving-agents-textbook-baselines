# Write your solution here. Read from stdin, write to stdout.

n = int(input())
s = list(map(int, input().split()))

# Convert to set for O(1) lookup
s_set = set(s)

count = 0

# For each element B, check all possible A values
for b in s:
    for a in s:
        if a < b:
            # Calculate C = 2B - A
            c = 2 * b - a
            # Check if C exists in set and C > B
            if c in s_set and c > b:
                count += 1

print(count)
