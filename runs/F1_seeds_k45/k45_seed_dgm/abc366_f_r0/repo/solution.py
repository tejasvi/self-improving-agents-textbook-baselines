from itertools import permutations

# Read input
N, K = map(int, input().split())
functions = []
for _ in range(N):
    a, b = map(int, input().split())
    functions.append((a, b))

# Try all permutations of K distinct indices from 0 to N-1
max_value = float('-inf')

# Generate all permutations of K distinct indices from range [0, N-1]
for perm in permutations(range(N), K):
    # Start with x = 1
    x = 1
    
    # Apply functions in order from perm
    for func_idx in perm:
        a, b = functions[func_idx]
        x = a * x + b
    
    # Track maximum
    max_value = max(max_value, x)

print(max_value)
