# Write your solution here. Read from stdin, write to stdout.

def mod_pow(base, exp, mod):
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
    MOD = 998244353
    
    # Chromatic polynomial for a cycle: P(N, M) = (M-1)^N + (-1)^N * (M-1)
    # This counts the number of ways to color N vertices in a cycle with M colors
    # such that no two adjacent vertices have the same color
    
    # Compute (M-1)^N mod MOD
    term1 = mod_pow(M - 1, N, MOD)
    
    # Compute (-1)^N * (M-1) mod MOD
    if N % 2 == 0:
        # (-1)^N = 1 when N is even
        term2 = (M - 1) % MOD
    else:
        # (-1)^N = -1 when N is odd
        term2 = (-(M - 1)) % MOD
    
    # Result = (M-1)^N + (-1)^N * (M-1)
    result = (term1 + term2) % MOD
    return result

# Read input
N, M = map(int, input().split())

# Solve and print
print(solve(N, M))
