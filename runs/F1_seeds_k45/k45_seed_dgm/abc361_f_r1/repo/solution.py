import math

def count_perfect_powers(N):
    if N < 2:
        return 1 if N == 1 else 0
    
    # For each base a, compute the maximum b such that a^b <= N
    # Then we need to count unique values
    
    # Key insight: use inclusion-exclusion with Möbius function
    # A number n is counted as:
    # - a perfect square (b=2) if it can be written as m^2
    # - a perfect cube (b=3) if it can be written as m^3
    # - etc.
    
    # But 2^6 = 64 is both a perfect square AND a perfect cube
    # We want to count each number exactly once
    
    # Using Möbius function:
    # count = sum over all b >= 2 of: mu(b) * (number of a^b <= N)
    # where mu is the Möbius function
    
    def mobius(n):
        """Compute Möbius function"""
        if n == 1:
            return 1
        
        # Check for squared prime factors
        temp = n
        factors = []
        d = 2
        while d * d <= temp:
            if temp % d == 0:
                factors.append(d)
                temp //= d
                if temp % d == 0:  # squared factor
                    return 0
            d += 1
        if temp > 1:
            factors.append(temp)
        
        # Return (-1)^k where k is number of prime factors
        return (-1) ** len(factors)
    
    def int_root(N, b):
        """Compute floor(N^(1/b)) safely for large N"""
        if b == 1:
            return N
        
        # Use binary search for better accuracy
        low, high = 1, int(N ** (1.0 / b)) + 2
        
        while low < high:
            mid = (low + high + 1) // 2
            if mid ** b <= N:
                low = mid
            else:
                high = mid - 1
        
        return low
    
    result = 0
    max_b = 63  # Since 2^63 > 10^18
    
    for b in range(1, max_b + 1):
        count_b = int_root(N, b)
        mu_b = mobius(b)
        result += mu_b * count_b
    
    return result

N = int(input())
print(count_perfect_powers(N))
