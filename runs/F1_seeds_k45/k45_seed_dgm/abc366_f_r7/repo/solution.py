# Write your solution here. Read from stdin, write to stdout.

def solve():
    # Read input
    N, K = map(int, input().split())
    functions = []
    for _ in range(N):
        A, B = map(int, input().split())
        functions.append((A, B))
    
    max_value = float('-inf')
    
    # Generate all permutations of K functions from N functions
    # and compute the composed result
    def backtrack(current_permutation, used):
        nonlocal max_value
        
        if len(current_permutation) == K:
            # Compute f_{p_1}(f_{p_2}(...f_{p_K}(1)...))
            value = 1
            # Apply functions in reverse order of the permutation
            # because we compose from inside out
            for i in range(K - 1, -1, -1):
                func_idx = current_permutation[i]
                A, B = functions[func_idx]
                value = A * value + B
            max_value = max(max_value, value)
            return
        
        # Try adding each unused function
        for i in range(N):
            if i not in used:
                used.add(i)
                current_permutation.append(i)
                backtrack(current_permutation, used)
                current_permutation.pop()
                used.remove(i)
    
    backtrack([], set())
    print(max_value)

solve()
