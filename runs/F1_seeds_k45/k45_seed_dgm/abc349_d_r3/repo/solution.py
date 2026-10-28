def solve(L, R):
    """
    Divide S(L, R) into minimum number of good sequences.
    A good sequence is S(2^i * j, 2^i * (j+1)) for non-negative integers i, j.
    This means a range [l, r) where:
    - r - l = 2^i (the length is a power of 2)
    - l is divisible by 2^i
    """
    segments = []
    l = L
    
    while l < R:
        # Find the largest power of 2 that we can use for the next segment
        # We want to maximize r = l + 2^i such that:
        # 1. l is divisible by 2^i
        # 2. r <= R
        
        # Start from the highest possible power of 2 and work downwards
        best_r = l + 1  # At minimum, we can always take a segment of length 1
        
        # The maximum power is limited by l's divisibility and (R - l)
        power = 1
        while power <= R - l:
            # Check if l is divisible by power and l + power <= R
            if l % power == 0:
                best_r = l + power
            power <<= 1
        
        segments.append((l, best_r))
        l = best_r
    
    return segments

# Read input
L, R = map(int, input().split())

# Solve
segments = solve(L, R)

# Output
print(len(segments))
for l, r in segments:
    print(l, r)
