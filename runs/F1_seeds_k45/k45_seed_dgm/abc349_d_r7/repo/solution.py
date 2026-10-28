# Write your solution here. Read from stdin, write to stdout.

def solve(L, R):
    """
    Divide S(L, R) into minimum number of good sequences.
    A good sequence S(l, r) has l = 2^i * j and r = 2^i * (j+1)
    which means r - l = 2^i and l is divisible by 2^i.
    """
    result = []
    current = L
    
    while current < R:
        # Find the largest power of 2 such that:
        # 1. current is divisible by that power of 2
        # 2. current + that power of 2 <= R
        
        best_length = 1  # At least S(current, current+1) is always good
        
        # Try powers of 2 from largest to smallest
        for i in range(60, -1, -1):
            power_of_2 = 1 << i
            # Check if current is divisible by power_of_2
            if current % power_of_2 == 0:
                # Then S(current, current + power_of_2) could be a good sequence
                next_pos = current + power_of_2
                if next_pos <= R:
                    best_length = power_of_2
                    break
        
        next_current = current + best_length
        result.append((current, next_current))
        current = next_current
    
    return result

# Read input
L, R = map(int, input().split())

# Solve
sequences = solve(L, R)

# Print output
print(len(sequences))
for l, r in sequences:
    print(l, r)
