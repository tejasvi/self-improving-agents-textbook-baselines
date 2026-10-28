# Write your solution here. Read from stdin, write to stdout.

def solve(N, M):
    sequences = []
    
    def backtrack(position, current_sequence, last_value):
        """
        position: current position we're filling (1-indexed)
        current_sequence: list of values selected so far
        last_value: the last value selected (or 0 if none)
        """
        if position > N:
            # We've filled all N positions
            sequences.append(current_sequence[:])
            return
        
        # Determine the minimum value for the current position
        if position == 1:
            min_val = 1
        else:
            min_val = last_value + 10
        
        # Determine the maximum value for the current position
        if position == N:
            # Last position must be <= M
            max_val = M
        else:
            # Not the last position, but we need to ensure future positions can reach M
            # For position i, we need at least (N - i) * 10 more to be added to reach valid end
            # So: current_value + (N - i) * 10 <= M
            # current_value <= M - (N - i) * 10
            remaining_positions = N - position
            max_val = M - remaining_positions * 10
        
        # Try all valid values at this position
        for val in range(min_val, max_val + 1):
            current_sequence.append(val)
            backtrack(position + 1, current_sequence, val)
            current_sequence.pop()
    
    backtrack(1, [], 0)
    return sequences

# Read input
N, M = map(int, input().split())

# Generate all valid sequences
sequences = solve(N, M)

# Output
print(len(sequences))
for seq in sequences:
    print(' '.join(map(str, seq)))
