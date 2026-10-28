# Write your solution here. Read from stdin, write to stdout.

def solve():
    # Read input
    N, K = map(int, input().split())
    functions = []
    for _ in range(N):
        A, B = map(int, input().split())
        functions.append((A, B))
    
    # DFS to explore all permutations of K distinct functions
    max_value = float('-inf')
    
    def dfs(current_value, used_mask, depth):
        nonlocal max_value
        
        # If we've applied K functions, update max value
        if depth == K:
            max_value = max(max_value, current_value)
            return
        
        # Try each function that hasn't been used yet
        for i in range(N):
            if not (used_mask & (1 << i)):
                # Apply function i: f_i(x) = A_i * x + B_i
                A, B = functions[i]
                new_value = A * current_value + B
                
                # Mark function i as used and continue DFS
                new_mask = used_mask | (1 << i)
                dfs(new_value, new_mask, depth + 1)
    
    # Start DFS from x = 1
    dfs(1, 0, 0)
    
    print(max_value)

solve()
