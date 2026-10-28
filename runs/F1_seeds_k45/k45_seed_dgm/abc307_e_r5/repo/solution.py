# Write your solution here. Read from stdin, write to stdout.

MOD = 998244353

def mod_pow(base, exp, mod):
    """Compute base^exp mod mod efficiently"""
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
    Count the number of ways to assign integers 0 to M-1 to N people
    standing in a circle such that no two adjacent people have the same integer.
    
    This is the chromatic polynomial for a cycle graph C_N with M colors:
    P(N, M) = (M-1)^N + (-1)^N * (M-1)
    """
    
    # Compute (M-1)^N mod MOD
    term1 = mod_pow(M - 1, N, MOD)
    
    # Compute (-1)^N * (M-1) mod MOD
    if N % 2 == 0:
        # (-1)^N = 1 when N is even
        term2 = (M - 1) % MOD
    else:
        # (-1)^N = -1 when N is odd
        term2 = (-(M - 1)) % MOD
    
    # Result = term1 + term2
    result = (term1 + term2) % MOD
    return result

# Read input
N, M = map(int, input().split())

# Solve and print result
print(solve(N, M))
