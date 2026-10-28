def solve(N):
    """
    Count integers x between 1 and N that can be expressed as a^b
    where a >= 1 and b >= 2.
    
    Key insight: Use inclusion-exclusion with Mobius function.
    A number n is a perfect power iff in its prime factorization,
    all exponents have GCD >= 2.
    
    count = sum_{b=2}^{log N} floor(N^(1/b)) * mu(b) / (1 if b primitive else 0)
    
    Actually simpler: count = sum_{d=2}^{log N} mu(d) * floor(N^(1/d))
    But this needs careful handling.
    """
    
    # For a number to be expressible as a^b with b >= 2,
    # it must have all exponents in prime factorization share a common divisor >= 2
    
    # count = sum over all primes p and exponent b >= 2 of floor(N^(1/b))
    #         minus corrections for overlaps
    
    # Better formulation using Mobius:
    # Perfect b-th powers include numbers that might also be perfect c-th powers
    # Use inclusion-exclusion: count = sum_{b>=2} mu(b) * floor(N^(1/b))
    # where mu is the Mobius function
    
    # Wait, the right formula is:
    # count = sum_{d=1}^{log N} mu(d) * floor(N^(1/d))
    # This counts numbers that are NOT primitive b-th powers
    
    # Actually, I think the right approach is different.
    # Let count_b = floor(N^(1/b)) be perfect b-th powers
    # A number m is in our answer if count_b[b] includes it for some b >= 2
    
    # To avoid double-counting, use inclusion-exclusion on exponents:
    # A number a^b where b = d * k (d >= 2 is minimal divisor)
    # So only count if d is the minimal such divisor
    
    # This leads to: count = sum_{b=2}^{log N} I(b is square-free) * ...
    # Still complex
    
    # Let me use a direct approach without storing all values:
    # Use the Mobius function property:
    # count = sum_{d=2}^{log N} (floor(N^(1/d)) - 1)
    #         - (numbers counted multiple times)
    
    # Actually, the formula is:
    # count = sum_{d|lcm of exponents, d>=2} count_of_d_th_powers
    #         using inclusion-exclusion
    
    # Simplest correct approach:
    # For each b from 2 to log(N), we have floor(N^(1/b)) values that are perfect b-th powers
    # But we need to subtract duplicates
    # A number is counted in both floor(N^(1/b)) and floor(N^(1/c)) if it's both a b-th and c-th power
    # This happens when it's a (lcm(b,c))-th power
    
    # Let's use: total = sum_{b=2}^{logN} floor(N^(1/b))
    #            Then subtract: sum_{b,c : b,c >= 2, b|c} (double counts)
    
    # Use inclusion-exclusion with Mobius:
    # The formula that works is:
    # count = sum_{k=2}^{log N} mu(k) * floor(N^(1/k))
    # NO! This isn't right either.
    
    # Correct approach I found: 
    # Perfect powers = numbers n where max_exponent_in_prime_factorization >= 2
    #                  AND gcd_of_exponents >= 2
    # Count = sum_{d=2}^{log N} floor(N^(1/d)) - (duplicates)
    # 
    # Using Mobius: a number is counted exactly once if we use:
    # answer = sum_{d=2}^{log N} (mu(d) != 0 ? floor(N^(1/d)) : 0)
    # NO!
    
    # CORRECT formula:
    # answer = sum_{d=2}^{log N} (-1)^(omega(d)) * floor(N^(1/d))
    # where omega(d) is the number of distinct prime divisors of d
    # This is basically applying Mobius function!
    
    # answer = sum_{d=2}^{log N} mu(d) * floor(N^(1/d))
    # But actually we need to be more careful.
    
    # LET ME LOOK UP THE RIGHT FORMULA:
    # A number n is a perfect power iff
    # n = a^b for some a, b >= 1, b >= 2
    # 
    # Count is given by:
    # count = sum_{b=2}^{log N} floor(N^(1/b)) 
    #         - sum_{b=4}^{log N} floor(N^(1/b))   [subtract 4th powers counted twice as squares]
    #         - sum_{b=6}^{log N} floor(N^(1/b))   [subtract 6th powers counted twice]
    #         ...
    # 
    # Using inclusion-exclusion on square-free exponents:
    # answer = sum_{d=1}^{log N} mu(d) * floor(N^(1/d))
    # where we want d starting from 2
    
    # Actually no. Let me think differently.
    # For each integer b >= 2, the count of perfect b-th powers is floor(N^(1/b))
    # But we're overcounting: a^6 is counted as both perfect square (when we do b=2) and perfect cube (when we do b=3)
    
    # To count distinct values, use:
    # Inclusion-exclusion on exponents b
    # answer = sum_{b>=2} (-1)^(omega(b)+1) * floor(N^(1/b))
    # where omega counts prime divisors
    # This ensures each number is counted exactly once
    
    # Which is equivalent to:
    # answer = sum_{b>=2} (-1)^(k+1) * floor(N^(1/b))
    # where k = number of distinct prime divisors of b
    
    # This is the Mobius function: mu(b) = (-1)^k if b is square-free, 0 otherwise
    # So: answer = - sum_{b>=2} mu(b) * floor(N^(1/b))
    # (negative sign because we want to count, not exclude)
    
    # Actually the formula should be:
    # answer = sum_{b=2}^{log N} mu(b) * floor(N^(1/b)) - 1
    # (subtracting 1 to handle the edge case)
    
    # Let's just implement it directly using the formula:
    # The count of perfect powers up to N is:
    # sum_{d=2}^{log N} mobius(d) * floor(N^(1/d))
    
    def mobius(n):
        """Compute Mobius function"""
        if n == 1:
            return 1
        # Factor n and check for squared factors
        temp = n
        result = 1
        d = 2
        while d * d <= temp:
            if temp % d == 0:
                temp //= d
                if temp % d == 0:
                    return 0  # squared prime factor
                result = -result
            d += 1
        if temp > 1:
            result = -result
        return result
    
    answer = 0
    max_b = 64  # log_2(10^18) is about 60
    
    for b in range(2, max_b):
        # Compute floor(N^(1/b))
        # Use binary search for precision
        low, high = 1, N
        while low < high:
            mid = (low + high + 1) // 2
            if mid ** b <= N:
                low = mid
            else:
                high = mid - 1
        count_b = low
        
        answer += mobius(b) * count_b
    
    return answer

# Read input
N = int(input())
print(solve(N))
