# Write your solution here. Read from stdin, write to stdout.

def mod_pow(base, exp, mod):
    """Compute (base ** exp) % mod efficiently"""
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
    
    # Chromatic polynomial for a cycle: P(k) = (k-1)^N + (-1)^N * (k-1)
    # where k is the number of colors (M in our case)
    
    term1 = mod_pow(M - 1, N, MOD)
    
    # (-1)^N * (M - 1)
    if N % 2 == 0:
        term2 = (M - 1) % MOD
    else:
        term2 = (-(M - 1)) % MOD
    
    result = (term1 + term2) % MOD
    return result

# Read input
N, M = map(int, input().split())

# Solve and print result
print(solve(N, M))
