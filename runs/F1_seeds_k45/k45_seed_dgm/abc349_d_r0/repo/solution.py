def solve(L, R):
    """
    Divide S(L, R) into the minimum number of good sequences.
    A good sequence is S(2^i * j, 2^i * (j+1)) for non-negative i, j.
    """
    
    def get_max_good_extension(l, R):
        """
        Given a starting position l, find the maximum r <= R such that
        S(l, r) is a good sequence.
        
        A good sequence S(l, r) requires:
        - r - l is a power of 2 (say 2^i)
        - l is divisible by 2^i (i.e., l = 2^i * j for some integer j)
        """
        # Try all powers of 2 in decreasing order
        # Start from the largest possible power and work down
        
        max_power = 60  # 2^60 is larger than our constraint (2^60)
        
        for i in range(max_power, -1, -1):
            length = 1 << i  # 2^i
            
            # Check if l is divisible by length
            if l % length != 0:
                continue
            
            r = l + length
            if r <= R:
                return r
        
        # Should never happen if constraints are satisfied
        return -1
    
    # Greedy division: always extend as far as possible
    divisions = []
    current = L
    
    while current < R:
        next_pos = get_max_good_extension(current, R)
        
        if next_pos == -1:
            # This shouldn't happen with valid input
            break
        
        divisions.append((current, next_pos))
        current = next_pos
    
    return divisions


def main():
    L, R = map(int, input().split())
    
    divisions = solve(L, R)
    
    print(len(divisions))
    for l, r in divisions:
        print(l, r)


if __name__ == "__main__":
    main()
