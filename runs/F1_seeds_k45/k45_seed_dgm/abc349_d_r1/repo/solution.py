def is_good_sequence(l, r):
    """
    Check if S(l, r) is a good sequence.
    S(l, r) is good if l = 2^i * j and r = 2^i * (j+1) for some non-negative i, j.
    This means r - l = 2^i and both l and r must be divisible by 2^i.
    """
    if l >= r:
        return False
    
    length = r - l
    
    # Check if length is a power of 2
    if length & (length - 1) != 0:
        return False
    
    # length is a power of 2, so length = 2^i
    # Now check if both l and r are divisible by length
    if l % length == 0 and r % length == 0:
        return True
    
    return False


def find_longest_good_sequence(pos, upper_limit):
    """
    Find the longest good sequence starting at pos.
    Returns the end point r such that S(pos, r) is a good sequence.
    """
    best_r = pos + 1  # At minimum, we can always form S(pos, pos+1) which is S(2^0*pos, 2^0*(pos+1))
    
    # Try all possible powers of 2 as the length
    power_of_2 = 1
    while pos + power_of_2 <= upper_limit:
        r = pos + power_of_2
        
        # Check if S(pos, r) is a good sequence
        if is_good_sequence(pos, r):
            best_r = r
        
        power_of_2 *= 2
    
    return best_r


def solve(L, R):
    """
    Divide S(L, R) into the minimum number of good sequences.
    """
    sequences = []
    current = L
    
    while current < R:
        next_pos = find_longest_good_sequence(current, R)
        sequences.append((current, next_pos))
        current = next_pos
    
    return sequences


def main():
    L, R = map(int, input().split())
    sequences = solve(L, R)
    
    print(len(sequences))
    for l, r in sequences:
        print(l, r)


if __name__ == "__main__":
    main()
