import itertools

def solve():
    # Read input
    N, K = map(int, input().split())
    functions = []
    for _ in range(N):
        A, B = map(int, input().split())
        functions.append((A, B))
    
    # Find the maximum value
    max_value = float('-inf')
    
    # Generate all permutations of K distinct indices from 0 to N-1
    for perm in itertools.permutations(range(N), K):
        # Apply the composed function starting from 1
        # f_{p_1}(f_{p_2}(...f_{p_K}(1)...))
        # We apply f_{p_K} first, then f_{p_{K-1}}, etc.
        value = 1
        for i in range(K - 1, -1, -1):
            A, B = functions[perm[i]]
            value = A * value + B
        
        max_value = max(max_value, value)
    
    print(max_value)

solve()
