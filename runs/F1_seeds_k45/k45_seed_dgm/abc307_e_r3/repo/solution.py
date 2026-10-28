# Write your solution here. Read from stdin, write to stdout.

MOD = 998244353

def pow_mod(base, exp, mod):
    """Compute (base^exp) % mod efficiently"""
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

def solve(N, M):
    """
    Calculate the chromatic polynomial for a cycle graph with N vertices and M colors.
    Formula: P(N, M) = (M-1)^N + (-1)^N * (M-1)
    """
    # Calculate (M-1)^N mod MOD
    term1 = pow_mod(M - 1, N, MOD)
    
    # Calculate (-1)^N * (M-1) mod MOD
    term2 = (M - 1) % MOD
    if N % 2 == 1:
        term2 = (-term2) % MOD
    
    # Add the two terms
    result = (term1 + term2) % MOD
    return result

# Read input
N, M = map(int, input().split())

# Solve and print the result
print(solve(N, M))
