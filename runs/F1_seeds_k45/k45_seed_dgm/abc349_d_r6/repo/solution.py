def solve(L, R):
    """
    Divide S(L, R) into the minimum number of good sequences.
    A good sequence S(l, r) satisfies: l = 2^i * j, r = 2^i * (j+1)
    This means: r - l = 2^i (power of 2), and l % (r-l) == 0
    """
    sequences = []
    current = L
    
    while current < R:
        # Find the longest good sequence starting at 'current'
        # We need to find the largest power of 2 such that:
        # 1. (current + 2^i) <= R
        # 2. current % 2^i == 0
        
        # Start with the smallest power of 2 and grow
        power = 1
        best_power = 1
        
        while current + power <= R:
            # Check if current is aligned to this power of 2
            if current % power == 0:
                best_power = power
            power *= 2
        
        # Add the sequence
        sequences.append((current, current + best_power))
        current += best_power
    
    return sequences

def main():
    L, R = map(int, input().split())
    sequences = solve(L, R)
    
    print(len(sequences))
    for l, r in sequences:
        print(l, r)

if __name__ == "__main__":
    main()
