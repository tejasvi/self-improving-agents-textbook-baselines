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
    Find the number of ways to color a cycle of N vertices with M colors
    such that no two adjacent vertices have the same color.
    
    This uses the chromatic polynomial for a cycle:
    P(N, M) = (M-1)^N + (-1)^N * (M-1)
    """
    # Compute (M-1)^N mod MOD
    term1 = pow_mod(M - 1, N, MOD)
    
    # Compute (-1)^N * (M-1) mod MOD
    if N % 2 == 0:
        # (-1)^N = 1 when N is even
        term2 = (M - 1) % MOD
    else:
        # (-1)^N = -1 when N is odd
        term2 = (-(M - 1)) % MOD
    
    # Add the terms
    result = (term1 + term2) % MOD
    return result

# Read input
N, M = map(int, input().split())

# Solve and print result
print(solve(N, M))
