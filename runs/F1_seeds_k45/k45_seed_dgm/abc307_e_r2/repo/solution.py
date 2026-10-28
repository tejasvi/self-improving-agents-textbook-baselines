# Solution for Distinct Adjacent problem
# The chromatic polynomial for a cycle of N vertices with M colors is:
# P(N, M) = (M-1)^N + (-1)^N * (M-1)

MOD = 998244353

def pow_mod(base, exp, mod):
    """Calculate base^exp % mod efficiently using binary exponentiation"""
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

def solve(N, M):
    """Calculate the number of ways to color N people in a circle with M colors"""
    # Formula: (M-1)^N + (-1)^N * (M-1)
    
    # Calculate (M-1)^N mod MOD
    term1 = pow_mod(M - 1, N, MOD)
    
    # Calculate (-1)^N * (M-1) mod MOD
    # (-1)^N is 1 if N is even, -1 if N is odd
    if N % 2 == 0:
        term2 = (M - 1) % MOD
    else:
        term2 = (-(M - 1)) % MOD
    
    # Add the two terms modulo MOD
    result = (term1 + term2) % MOD
    return result

# Read input
N, M = map(int, input().split())

# Solve and print the answer
print(solve(N, M))
