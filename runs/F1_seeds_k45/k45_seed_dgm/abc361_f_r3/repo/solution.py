def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def count_b_th_powers(b, N):
    """Count how many b-th powers are <= N"""
    # Find largest a such that a^b <= N
    # Use Newton's method or direct computation for safety
    if b == 1:
        return N
    
    # Start with an estimate
    a = int(N ** (1.0 / b)) + 1
    
    # Adjust downward if needed
    while a > 0 and a ** b > N:
        a -= 1
    
    # Check if we can go one step higher
    if (a + 1) ** b <= N:
        a += 1
    
    return a

def solve(N):
    """Count perfect powers <= N using inclusion-exclusion"""
    
    memo = {}
    def f(b):
        """Count b-th powers <= N"""
        if b not in memo:
            memo[b] = count_b_th_powers(b, N)
        return memo[b]
    
    # Prime exponents to use in inclusion-exclusion
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]
    
    result = 0
    
    # For each non-empty subset of primes, compute the LCM and use inclusion-exclusion
    for mask in range(1, 2 ** len(primes)):
        lcm_val = 1
        count_primes = 0
        valid = True
        
        for i in range(len(primes)):
            if mask & (1 << i):
                p = primes[i]
                lcm_val = lcm_val * p // gcd(lcm_val, p)
                count_primes += 1
                
                # Early termination
                if lcm_val > 100:
                    valid = False
                    break
        
        if valid:
            count = f(lcm_val)
            # Inclusion-exclusion with Möbius-like coefficient
            if count_primes % 2 == 1:
                result += count
            else:
                result -= count
    
    return result

N = int(input())
print(solve(N))
