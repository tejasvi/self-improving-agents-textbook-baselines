import math
from math import gcd
from functools import reduce

def count_perfect_powers(N):
    """
    Count integers x in [1, N] that can be expressed as a^b 
    where a, b are positive integers and b >= 2.
    """
    
    if N == 1:
        return 1
    
    # Maximum exponent we need to consider
    max_exp = 64  # 2^64 > 10^18
    
    # For each exponent b from 2 to max_exp, 
    # count how many numbers are perfect b-th powers
    count = {}
    
    for b in range(2, max_exp):
        # Count numbers that are perfect b-th powers
        max_a = int(N ** (1.0 / b)) + 1
        
        # Binary search for exact count (to handle floating point errors)
        left, right = 1, max_a
        while left < right:
            mid = (left + right + 1) // 2
            if mid ** b <= N:
                left = mid
            else:
                right = mid - 1
        
        count[b] = left
        
        if left == 0 or left == 1:
            # No new perfect b-th powers beyond 1
            break
    
    # Now use inclusion-exclusion to avoid double counting
    # A number that is a perfect b-th power AND a perfect c-th power
    # is a perfect lcm(b,c)-th power
    
    # More elegant approach: use a set for small enough N, 
    # but that won't work for 10^18
    
    # Better approach: For each number of the form a^b, 
    # we should count it only once. 
    # A number x = a^b can also be written as x = (a^(b/d))^d for divisors d of b
    # So we should count x for the minimal b (the exponent in prime factorization)
    
    # Use Mobius function / inclusion-exclusion
    # Count of integers that are perfect b-th powers where gcd of all 
    # exponent divisors equals b (primitive b-th powers)
    
    result = 0
    
    # For each exponent b, count perfect b-th powers
    # But subtract those that are also perfect c-th powers for c < b
    # where c divides b... actually this is complex
    
    # Simpler: use inclusion-exclusion on exponents
    # If b divides c, then every perfect c-th power is also a perfect b-th power
    
    from collections import defaultdict
    
    # Use inclusion-exclusion principle
    exp_count = defaultdict(int)
    
    # First, collect counts for each exponent
    for b in range(2, max_exp):
        max_a = int(N ** (1.0 / b)) + 1
        left, right = 1, max_a
        while left < right:
            mid = (left + right + 1) // 2
            if mid ** b <= N:
                left = mid
            else:
                right = mid - 1
        exp_count[b] = left
    
    # Apply inclusion-exclusion
    # A number is counted in exp_count[b] and exp_count[c] if it's 
    # a perfect lcm(b,c)-th power
    
    # Let's use a different approach: Mobius inversion
    # Let f(b) = count of perfect b-th powers <= N
    # Let g(b) = count of numbers that are perfect b-th powers but not 
    #            perfect c-th powers for any proper divisor c of b
    # Then g(b) = f(b) - sum(g(d) for d|b, d<b)
    # And answer = sum(g(b))
    
    # Find all relevant exponents
    exponents = []
    for b in range(2, max_exp):
        if exp_count[b] > 1:
            exponents.append(b)
        else:
            break
    
    # Get divisors of each exponent
    def get_divisors(n):
        divisors = []
        for i in range(1, int(math.sqrt(n)) + 1):
            if n % i == 0:
                divisors.append(i)
                if i != n // i:
                    divisors.append(n // i)
        return sorted(divisors)
    
    # Apply inclusion-exclusion
    primitive = {}
    for b in exponents:
        primitive[b] = exp_count[b]
        divisors = get_divisors(b)
        for d in divisors:
            if d < b and d in primitive:
                primitive[b] -= primitive[d]
    
    result = sum(primitive.values())
    return result

N = int(input())
print(count_perfect_powers(N))
