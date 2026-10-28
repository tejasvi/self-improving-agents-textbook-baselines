# Write your solution here. Read from stdin, write to stdout.

MOD = 998244353

def power(base, exp, mod):
    """Compute (base^exp) % mod using fast exponentiation"""
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
    For a cycle of length N with M colors, the chromatic polynomial is:
    P(N, M) = (M-1)^N + (-1)^N * (M-1)
    """
    if M == 0:
        return 0
    
    # Compute (M-1)^N mod MOD
    term1 = power(M - 1, N, MOD)
    
    # Compute (-1)^N * (M-1)
    if N % 2 == 0:
        # Even N: (-1)^N = 1
        term2 = (M - 1) % MOD
    else:
        # Odd N: (-1)^N = -1
        term2 = (-(M - 1)) % MOD
    
    result = (term1 + term2) % MOD
    return result

# Read input
N, M = map(int, input().split())

# Compute and print result
print(solve(N, M))
