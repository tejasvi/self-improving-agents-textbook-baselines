def get_max_power_of_2_divisor(n):
    """Get the largest power of 2 that divides n (i.e., the value 2^i where 2^i divides n)"""
    if n == 0:
        return 1
    # Find the largest power of 2 dividing n
    power = 1
    while n % (power * 2) == 0:
        power *= 2
    return power

def find_next_breakpoint(l, r_max):
    """
    Find the largest r <= r_max such that S(l, r) is a good sequence.
    
    A sequence S(l, r) is good if it can be represented as S(2^i*j, 2^i*(j+1))
    This means:
    - The length (r - l) must be a power of 2
    - Both l and r must be multiples of (r - l)
    """
    # The maximum power of 2 that can divide l determines the initial length
    # We need to find the largest power of 2 such that l is a multiple of it
    # and we can extend the sequence to a multiple of it
    
    max_power = get_max_power_of_2_divisor(l)
    
    # Start with the maximum power of 2 that divides l
    # Try progressively larger powers of 2
    length = max_power
    
    while length * 2 <= r_max - l:
        # Check if we can extend to length * 2
        # This requires (l + length * 2) to be a multiple of (length * 2)
        # i.e., l must be a multiple of (length * 2)
        if (l + length * 2) <= r_max and l % (length * 2) == 0:
            length *= 2
        else:
            break
    
    return l + length

def solve(L, R):
    """Divide S(L, R) into the minimum number of good sequences."""
    sequences = []
    current_l = L
    
    while current_l < R:
        # Find the maximum r such that S(current_l, r) is good and r <= R
        current_r = find_next_breakpoint(current_l, R)
        sequences.append((current_l, current_r))
        current_l = current_r
    
    return sequences

# Read input
L, R = map(int, input().split())

# Solve
result = solve(L, R)

# Print output
print(len(result))
for l, r in result:
    print(l, r)
