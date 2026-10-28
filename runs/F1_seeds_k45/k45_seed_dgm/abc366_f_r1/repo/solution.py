from itertools import permutations

# Read input
N, K = map(int, input().split())
functions = []
for _ in range(N):
    A, B = map(int, input().split())
    functions.append((A, B))

# Try all permutations of K distinct functions chosen from N functions
max_value = float('-inf')

# Generate all permutations of K indices from range(N)
for perm in permutations(range(N), K):
    # Compute the composition f_{p_1}(f_{p_2}(...f_{p_K}(1)...))
    # Start with x = 1
    x = 1
    
    # Apply functions in reverse order: first apply f_{p_K}, then f_{p_{K-1}}, etc.
    for i in range(K - 1, -1, -1):
        func_idx = perm[i]
        A, B = functions[func_idx]
        x = A * x + B
    
    max_value = max(max_value, x)

print(max_value)
