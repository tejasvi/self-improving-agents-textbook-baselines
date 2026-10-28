from math import gcd

MOD = 998244353

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    # Precompute powers of 2
    pow2 = [1] * (N + 1)
    for i in range(1, N + 1):
        pow2[i] = (pow2[i-1] * 2) % MOD
    
    for m in range(1, N + 1):
        result = 0
        # For each pair (i, j) where i < j in A[0:m]
        for i in range(m):
            for j in range(i + 1, m):
                g = gcd(A[i], A[j])
                # Number of subsequences where positions i and j are consecutive
                # = 2^i * 2^(m-1-j)
                count = (pow2[i] * pow2[m - 1 - j]) % MOD
                contribution = (g * count) % MOD
                result = (result + contribution) % MOD
        
        print(result)

solve()
