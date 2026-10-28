#!/usr/bin/env python3

def count_perfect_powers(N):
    """
    Count integers x in [1, N] that can be expressed as x = a^b
    where a >= 1 and b >= 2.
    
    Key observation: x is a perfect power iff the GCD of exponents
    in its prime factorization is >= 2.
    
    Equivalently, x is perfect power iff x = m^k for some integer m and k >= 2.
    
    Approach:
    For each possible exponent k from 2 to 60:
    - Count how many k-th powers are <= N
    - These are numbers of form a^k where a >= 1
    - But avoid double counting using Möbius inversion
    
    The formula: a number is counted if it's a "primitive k-th power"
    (i.e., a^k where a is not itself a perfect power).
    
    Using Möbius: count of primitive k-th powers 
    = sum_{d|k} μ(k/d) * floor(N^(1/d))
    
    Total = sum_k (count of primitive k-th powers)
    """
    
    if N < 1:
        return 0
    
    def mobius(n):
        """Compute Möbius function for n"""
        if n == 1:
            return 1
        
        # Check for squared prime factors
        temp = n
        factors = 0
        d = 2
        while d * d <= temp:
            if temp % d == 0:
                temp //= d
                factors += 1
                if temp % d == 0:  # squared factor found
                    return 0
                # Continue to next prime
            d += 1
        if temp > 1:
            factors += 1
        
        return (-1) ** factors
    
    # Precompute floor(N^(1/d)) for all small d
    max_d = 64
    root = {}
    for d in range(1, max_d):
        # Binary search for largest a such that a^d <= N
        lo, hi = 1, min(N, int(N ** (1.0 / d)) + 2)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if mid ** d <= N:
                lo = mid
            else:
                hi = mid - 1
        root[d] = lo
    
    # Now count perfect powers
    # A number x is a perfect power if x = a^k for k >= 2
    # Sum over k >= 2 of (count of primitive k-th powers)
    
    result = 0
    for k in range(2, max_d):
        # Count primitive k-th powers
        # = sum_{d|k, d<k} μ(k/d) * floor(N^(1/d))
        
        primitive = 0
        d = 1
        while d <= k:
            if k % d == 0:
                factor = k // d
                if factor > 1:
                    contrib = mobius(factor) * root.get(d, 0)
                    primitive += contrib
            d += 1
        
        result += primitive
    
    return result


N = int(input())
print(count_perfect_powers(N))
