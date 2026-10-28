# Write your solution here. Read from stdin, write to stdout.

def solve(N, M):
    results = []
    
    def backtrack(pos, current_seq, last_value):
        """
        pos: current position (1-indexed) in the sequence
        current_seq: list of values built so far
        last_value: the value of the previous element
        """
        if pos == N + 1:
            # We've completed a sequence of length N
            results.append(current_seq[:])
            return
        
        if pos == 1:
            # First element: can be any value from 1 onwards
            # But we need to ensure we can still build a valid sequence
            # The minimum value for position N is: last_value + 10*(N-pos)
            # We need: last_value + 10*(N-pos) <= M
            min_val = 1
        else:
            # For position pos > 1, must be at least last_value + 10
            min_val = last_value + 10
        
        # Maximum value we can use at position pos
        # If pos == N, max is M (the final constraint)
        # If pos < N, we need to ensure we can still reach position N with values <= M
        # At position pos, if we use value v, then:
        # - position pos+1 needs at least v+10
        # - position N needs at least v + 10*(N-pos)
        # So: v + 10*(N-pos) <= M
        # Thus: v <= M - 10*(N-pos)
        max_val = M - 10 * (N - pos)
        
        for val in range(min_val, max_val + 1):
            current_seq.append(val)
            backtrack(pos + 1, current_seq, val)
            current_seq.pop()
    
    backtrack(1, [], 0)
    return results

# Read input
N, M = map(int, input().split())

# Solve
sequences = solve(N, M)

# Output
print(len(sequences))
for seq in sequences:
    print(' '.join(map(str, seq)))
