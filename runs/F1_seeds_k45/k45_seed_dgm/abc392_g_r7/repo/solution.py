# Write your solution here. Read from stdin, write to stdout.

n = int(input())
s = list(map(int, input().split()))

# Convert to set for O(1) lookup
s_set = set(s)

# Sort for easier iteration
s_sorted = sorted(s)

count = 0

# For each potential middle element B
for b in s_sorted:
    # For each potential left element A where A < B
    for a in s_sorted:
        if a >= b:
            break
        # Calculate what C should be: C = 2*B - A
        c = 2 * b - a
        # Check if C exists in the set and C > B
        if c in s_set and c > b:
            count += 1

print(count)
