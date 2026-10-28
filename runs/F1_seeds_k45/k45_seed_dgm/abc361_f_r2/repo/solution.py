def count_perfect_powers(N):
    """
    Count numbers that are a^b where a >= 1, b >= 2
    """
    
    # Key insight: Use Möbius function on exponents
    # The count is: sum of μ(b) * floor(N^(1/b)) for b >= 2
    # where μ is the Möbius function
    
    # Precompute which exponents up to 60 are NOT perfect powers
    # An exponent b is a perfect power iff b = c^k for some k >= 2
    
    def is_prime_power_free(n):
        """Check if n has no prime factors with exponent >= 2"""
        if n <= 1:
            return False
        
        # For b to be "bad" (a perfect power), it must be of form c^d where d >= 2
        # So we need to check if b can be factored as c^d
        
        # More specifically, b is bad if gcd of its prime factorization is > 1
        i = 2
        original_n = n
        factor_count = {}
        while i * i <= n:
            while n % i == 0:
                factor_count[i] = factor_count.get(i, 0) + 1
                n //= i
            i += 1
        if n > 1:
            factor_count[n] = factor_count.get(n, 0) + 1
        
        # Check if gcd of all exponents is 1
        from math import gcd
        from functools import reduce
        
        if not factor_count:
            return True
        exponents = list(factor_count.values())
        g = reduce(gcd, exponents)
        return g == 1
    
    total_count = 0
    
    # Iterate through exponents
    max_b = 60  # 2^60 > 10^18
    
    for b in range(2, max_b + 1):
        # Only count if b is not a perfect power
        if not is_prime_power_free(b):
            continue
        
        # Count how many a satisfy a^b <= N
        low, high = 1, 2 * 10**9
        while low < high:
            mid = (low + high + 1) // 2
            try:
                if mid ** b <= N:
                    low = mid
                else:
                    high = mid - 1
            except OverflowError:
                high = mid - 1
        
        total_count += low
    
    return total_count


N = int(input())
print(count_perfect_powers(N))
