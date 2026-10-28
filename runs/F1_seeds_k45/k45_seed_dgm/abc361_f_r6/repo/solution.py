import math

def count_perfect_powers(N):
    """
    Count integers x in [1, N] that can be expressed as x = a^b (b >= 2)
    """
    if N == 1:
        return 1  # Only 1 = 1^b for any b
    
    # We'll use a set to store all perfect powers to avoid duplicates
    perfect_powers = set()
    
    # The maximum exponent we need to consider is log2(N)
    max_exp = int(math.log2(N)) + 1
    
    # For each exponent from 2 to max_exp
    for b in range(2, max_exp + 1):
        # Maximum base a such that a^b <= N
        max_a = int(N ** (1.0 / b))
        
        # Check a few values around the floating point result
        # due to precision issues
        for a in range(max(1, max_a - 2), max_a + 3):
            power = a ** b
            if 1 <= power <= N:
                perfect_powers.add(power)
            if power > N:
                break
    
    return len(perfect_powers)

N = int(input())
print(count_perfect_powers(N))
