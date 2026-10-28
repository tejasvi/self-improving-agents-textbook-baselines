def solve(L, R):
    """
    Divide S(L, R) into the minimum number of good sequences.
    A good sequence S(l, r) can be represented as S(2^i * j, 2^i * (j+1)).
    
    Strategy: Greedy approach - at each step, find the longest good sequence
    starting from the current position.
    
    For a sequence S(l, r) to be good:
    - r - l = 2^i for some non-negative integer i
    - l = 2^i * j for some non-negative integer j
    - This means l must be divisible by (r - l)
    """
    segments = []
    current = L
    
    while current < R:
        # Find the longest good sequence starting at current
        # We need current = 2^i * j and current + 2^i <= R
        # So 2^i must divide current and current + 2^i <= R
        
        max_length = 1  # At minimum, 2^0 = 1 always works
        
        # Try increasing powers of 2
        i = 0
        while (1 << i) <= (R - current):  # 2^i <= R - current
            length = 1 << i  # 2^i
            if current % length == 0:
                max_length = length
            i += 1
        
        # Add the segment
        next_pos = current + max_length
        segments.append((current, next_pos))
        current = next_pos
    
    return segments

def main():
    L, R = map(int, input().split())
    segments = solve(L, R)
    
    print(len(segments))
    for l, r in segments:
        print(l, r)

if __name__ == "__main__":
    main()
