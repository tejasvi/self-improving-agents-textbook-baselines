# Write your solution here. Read from stdin, write to stdout.

def solve(N, M):
    sequences = []
    
    def backtrack(current_sequence):
        # If we've built a complete sequence
        if len(current_sequence) == N:
            sequences.append(current_sequence[:])
            return
        
        pos = len(current_sequence)
        
        # Determine the minimum value for this position
        if pos == 0:
            min_val = 1
        else:
            min_val = current_sequence[pos - 1] + 10
        
        # Determine the maximum value for this position
        # We need to ensure that there's enough "room" for the remaining elements
        # Each remaining element needs to be at least 10 more than the previous
        remaining_positions = N - pos - 1
        max_val = M - remaining_positions * 10
        
        # Try all valid values at this position in ascending order
        for val in range(min_val, max_val + 1):
            current_sequence.append(val)
            backtrack(current_sequence)
            current_sequence.pop()
    
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
