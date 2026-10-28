# Write your solution here. Read from stdin, write to stdout.

def solve():
    N, M = map(int, input().split())
    
    sequences = []
    
    def backtrack(current_sequence, position):
        # If we've built a complete sequence
        if position == N:
            sequences.append(current_sequence[:])
            return
        
        # Determine the minimum value for the next position
        if position == 0:
            min_val = 1
        else:
            min_val = current_sequence[position - 1] + 10
        
        # Determine the maximum value for the next position
        if position == N - 1:
            # Last position: must not exceed M
            max_val = M
        else:
            # Not the last position: we need to leave room for remaining elements
            # For position i, we need at least (N - 1 - i) more elements after
            # Each needs to be at least 10 more than the previous
            # So max_val should be at most M - 10 * (N - 1 - i)
            max_val = M - 10 * (N - 1 - position)
        
        # Try all valid values for this position
        for val in range(min_val, max_val + 1):
            current_sequence.append(val)
            backtrack(current_sequence, position + 1)
            current_sequence.pop()
    
    backtrack([], 0)
    
    # Print results
    print(len(sequences))
    for seq in sequences:
        print(' '.join(map(str, seq)))

solve()
