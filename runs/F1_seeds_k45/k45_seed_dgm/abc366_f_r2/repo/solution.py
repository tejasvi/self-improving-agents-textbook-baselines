from itertools import permutations

# Read input
N, K = map(int, input().split())
functions = []
for _ in range(N):
    A, B = map(int, input().split())
    functions.append((A, B))

# Generate all permutations of K distinct functions from N functions
# This gives us all possible sequences p of length K
max_value = float('-inf')

for perm in permutations(range(N), K):
    # Start with value 1
    value = 1
    # Apply functions in order: f_{p_1}(f_{p_2}(...f_{p_K}(1)...))
    # This means we apply f_{p_K} first, then f_{p_{K-1}}, etc.
    for i in range(K - 1, -1, -1):
        func_idx = perm[i]
        A, B = functions[func_idx]
        value = A * value + B
    
    max_value = max(max_value, value)

print(max_value)
