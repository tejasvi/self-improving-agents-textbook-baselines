def solve(N, M):
    sequences = []
    
    def backtrack(index, current_sequence, last_value):
        # Base case: we've filled all N positions
        if index == N:
            sequences.append(current_sequence[:])
            return
        
        # Determine the minimum value for this position
        if index == 0:
            min_value = 1
        else:
            min_value = last_value + 10
        
        # If this is the last position, max value is M
        if index == N - 1:
            max_value = M
        else:
            # For non-last positions, we need to ensure remaining positions can reach M
            # Position N-1 needs at least min_value + 10*(N-1-index)
            # So this position can be at most M - 10*(N-1-index)
            max_value = M - 10 * (N - 1 - index)
        
        # Try all values in the valid range
        for value in range(min_value, max_value + 1):
            current_sequence.append(value)
            backtrack(index + 1, current_sequence, value)
            current_sequence.pop()
    
    backtrack(0, [], 0)
    return sequences

# Read input
N, M = map(int, input().split())

# Solve and get sequences
sequences = solve(N, M)

# Output
print(len(sequences))
for seq in sequences:
    print(' '.join(map(str, seq)))
