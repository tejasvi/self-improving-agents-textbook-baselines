def solve(N, M):
    results = []
    
    def backtrack(current_sequence):
        # If we have N elements, check if the last one is valid
        if len(current_sequence) == N:
            if current_sequence[-1] <= M:
                results.append(current_sequence[:])
            return
        
        # Determine the minimum value for the next element
        if len(current_sequence) == 0:
            min_val = 1
        else:
            min_val = current_sequence[-1] + 10
        
        # Determine the maximum value we should try
        # We need to ensure that we can still fit N - len(current_sequence) more elements
        # If we have k more elements to add, each needs to be at least 10 more than the previous
        # So the minimum possible value for the last element would be:
        # min_val + 10 * (k - 1)
        # This must be <= M
        k = N - len(current_sequence)
        max_val = M - 10 * (k - 1)
        
        # Try all possible values for the next element
        for val in range(min_val, max_val + 1):
            current_sequence.append(val)
            backtrack(current_sequence)
            current_sequence.pop()
    
    backtrack([])
    return results

# Read input
N, M = map(int, input().split())

# Solve the problem
sequences = solve(N, M)

# Output
print(len(sequences))
for seq in sequences:
    print(' '.join(map(str, seq)))
