# Read input
N = int(input())
S = list(map(int, input().split()))

# Convert to set for O(1) lookup
S_set = set(S)

# Count fine triplets
count = 0

# Try each element as B (middle element)
for B in S:
    # For each element A < B, check if C = 2*B - A exists and C > B
    for A in S:
        if A < B:
            C = 2 * B - A
            # Check if C exists in the set and C > B
            if C > B and C in S_set:
                count += 1

print(count)
