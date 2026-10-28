import math

MOD = 998244353

def pow_mod(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    # For each m from 1 to N
    for m in range(1, N + 1):
        total_score = 0
        
        # For each pair (i, j) where i < j and both are < m
        for i in range(m):
            for j in range(i + 1, m):
                # These elements are consecutive in subsequences where:
                # - All elements between i and j (exclusive) are not selected
                # - We can choose any subset of elements before i and after j
                g = math.gcd(A[i], A[j])
                # Number of subsequences = 2^i * 2^(m-1-j)
                count = pow_mod(2, i + m - 1 - j, MOD)
                contribution = (g * count) % MOD
                total_score = (total_score + contribution) % MOD
        
        print(total_score)

solve()
