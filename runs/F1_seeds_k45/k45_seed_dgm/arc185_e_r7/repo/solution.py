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
        # For each pair (i, j) where 0 <= i < j < m (0-indexed)
        for i in range(m):
            for j in range(i + 1, m):
                g = gcd(A[i], A[j])
                # Count of subsequences where A[i] and A[j] are consecutive
                # Elements before i: i elements, choices: 2^i
                # Elements after j: (m-1-j) elements, choices: 2^(m-1-j)
                count = pow2[i] * pow2[m - 1 - j] % MOD
                result = (result + g * count) % MOD
        
        print(result)

solve()
