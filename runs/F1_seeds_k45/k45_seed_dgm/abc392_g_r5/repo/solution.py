# Write your solution here. Read from stdin, write to stdout.

n = int(input())
s = list(map(int, input().split()))

# Convert to set for O(1) lookup
s_set = set(s)
s_sorted = sorted(s)

count = 0

# For each possible middle element B
for b in s_sorted:
    # For each possible first element A
    for a in s_sorted:
        if a >= b:
            break
        # Calculate what C should be: A + C = 2B => C = 2B - A
        c = 2 * b - a
        # Check if C exists in the set and C > B
        if c in s_set and c > b:
            count += 1

print(count)
