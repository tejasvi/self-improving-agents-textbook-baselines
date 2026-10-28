import math

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def solve():
    MOD = 998244353
    N = int(input())
    A = list(map(int, input().split()))
    
    # Precompute powers of 2
    pow2 = [1] * (N + 1)
    for i in range(1, N + 1):
        pow2[i] = (pow2[i-1] * 2) % MOD
    
    # For each m from 1 to N
    for m in range(1, N + 1):
        answer = 0
        
        # For each pair (i, j) where i < j < m
        for i in range(m):
            for j in range(i + 1, m):
                g = gcd(A[i], A[j])
                # Number of subsequences where i and j are adjacent
                # We can choose any subset before i and any subset after j
                count = (pow2[i] * pow2[m - j - 1]) % MOD
                contribution = (g * count) % MOD
                answer = (answer + contribution) % MOD
        
        print(answer)

solve()
