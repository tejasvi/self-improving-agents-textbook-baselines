def solve():
    # Read input
    N, K = map(int, input().split())
    functions = []
    for _ in range(N):
        A, B = map(int, input().split())
        functions.append((A, B))
    
    # We need to find the maximum value of composing K distinct functions
    # Starting with value 1
    
    max_value = float('-inf')
    
    # Use backtracking to try all permutations of K distinct functions
    def backtrack(current_value, used, depth):
        nonlocal max_value
        
        if depth == K:
            # We've composed K functions, update max
            max_value = max(max_value, current_value)
            return
        
        # Try each function that hasn't been used yet
        for i in range(N):
            if i not in used:
                # Apply function i to current_value
                A, B = functions[i]
                new_value = A * current_value + B
                
                # Mark as used and recurse
                used.add(i)
                backtrack(new_value, used, depth + 1)
                used.remove(i)
    
    backtrack(1, set(), 0)
    print(max_value)

solve()
