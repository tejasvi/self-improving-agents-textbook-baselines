# Write your solution here. Read from stdin, write to stdout.

def solve():
    MOD = 998244353
    N, M = map(int, input().split())
    
    # Chromatic polynomial for a cycle: P(N, M) = (M-1)^N + (-1)^N * (M-1)
    # This counts the number of ways to color N vertices in a cycle with M colors
    # such that no two adjacent vertices have the same color
    
    # Calculate (M-1)^N mod MOD
    term1 = pow(M - 1, N, MOD)
    
    # Calculate (-1)^N * (M-1) mod MOD
    if N % 2 == 0:
        term2 = (M - 1) % MOD
    else:
        term2 = (-(M - 1)) % MOD
    
    # Result = term1 + term2
    result = (term1 + term2) % MOD
    
    print(result)

solve()
