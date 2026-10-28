def solve():
    N, M = map(int, input().split())
    
    sequences = []
    
    def backtrack(current_sequence, prev_value):
        # If we've built a complete sequence of length N
        if len(current_sequence) == N:
            if current_sequence[-1] <= M:
                sequences.append(current_sequence[:])
            return
        
        # We need to add more elements
        # The next element must be at least prev_value + 10
        # And we need to ensure the remaining elements can fit
        
        min_next = prev_value + 10 if prev_value > 0 else 1
        
        # Calculate the minimum possible value for the last element
        # if we start with min_next at the current position
        # Remaining positions: (N - len(current_sequence) - 1)
        remaining_positions = N - len(current_sequence) - 1
        min_last = min_next + (remaining_positions * 10)
        
        # If the minimum possible last element exceeds M, we can't continue
        if min_last > M:
            return
        
        # Try all possible values for the next element
        max_next = M - (remaining_positions * 10)
        
        for next_val in range(min_next, max_next + 1):
            current_sequence.append(next_val)
            backtrack(current_sequence, next_val)
            current_sequence.pop()
    
    # Start the backtracking
    backtrack([], 0)
    
    # Output results
    print(len(sequences))
    for seq in sequences:
        print(' '.join(map(str, seq)))

solve()
