# Write your solution here. Read from stdin, write to stdout.

def solve(N, M):
    sequences = []
    
    def backtrack(current_seq):
        # If we've built a complete sequence
        if len(current_seq) == N:
            sequences.append(current_seq[:])
            return
        
        # Determine the minimum value for the next element
        if len(current_seq) == 0:
            min_val = 1
        else:
            min_val = current_seq[-1] + 10
        
        # Determine the maximum value for the next element
        # We need to ensure that we can still fill the remaining positions
        remaining = N - len(current_seq) - 1  # positions left after adding next
        
        if remaining == 0:
            # This is the last element, it must be <= M
            max_val = M
        else:
            # We need A_N <= M
            # If we set current element to x, we need:
            # x + 10 * remaining <= M
            max_val = M - 10 * remaining
        
        # Try all valid values for the current position
        for val in range(min_val, max_val + 1):
            current_seq.append(val)
            backtrack(current_seq)
            current_seq.pop()
    
    backtrack([])
    return sequences

# Read input
N, M = map(int, input().split())

# Find all valid sequences
sequences = solve(N, M)

# Output
print(len(sequences))
for seq in sequences:
    print(' '.join(map(str, seq)))
