def solve():
    N, K = map(int, input().split())
    functions = []
    for _ in range(N):
        a, b = map(int, input().split())
        functions.append((a, b))
    
    # We need to find the maximum value when composing K functions
    # Start with value 1, and apply K distinct functions in some order
    
    max_result = float('-inf')
    
    # Generate all permutations of K functions from N functions
    # We can use itertools.permutations or recursion
    from itertools import permutations
    
    # Get all permutations of length K from indices 0 to N-1
    for perm in permutations(range(N), K):
        # perm is a tuple of K distinct indices
        # Apply functions in order: f[perm[0]](f[perm[1]](...f[perm[K-1]](1)...))
        
        value = 1
        # Apply functions from the last index to the first (reverse order)
        # Because composition f(g(x)) means apply g first, then f
        for i in range(K - 1, -1, -1):
            func_idx = perm[i]
            a, b = functions[func_idx]
            value = a * value + b
        
        max_result = max(max_result, value)
    
    print(max_result)

solve()
