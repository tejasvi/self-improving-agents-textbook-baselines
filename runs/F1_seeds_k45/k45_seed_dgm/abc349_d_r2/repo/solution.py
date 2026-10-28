def solve(L, R):
    """
    Divide S(L, R) into the minimum number of good sequences.
    
    A good sequence S(l, r) must satisfy:
    - l = 2^i * j for some non-negative integers i, j
    - r = 2^i * (j+1)
    - So it has length 2^i and starts at a multiple of 2^i
    """
    
    segments = []
    current = L
    
    while current < R:
        # Find the maximum power of 2 such that:
        # 1. current is divisible by 2^i
        # 2. current + 2^i <= R
        
        # Start with power of 2 = 1
        power = 1
        
        # Keep doubling as long as the conditions are met
        while True:
            next_power = power * 2
            # Check both conditions:
            # 1. current is divisible by next_power
            # 2. current + next_power <= R
            if next_power <= (R - current) and current % next_power == 0:
                power = next_power
            else:
                break
        
        # Now power is the maximum valid power of 2
        end = current + power
        segments.append((current, end))
        current = end
    
    return segments


# Read input
L, R = map(int, input().split())

# Solve
segments = solve(L, R)

# Print output
print(len(segments))
for l, r in segments:
    print(l, r)
