import math

MOD = 998244353

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    # Precompute powers of 2
    pow2 = [1] * (n + 1)
    for i in range(1, n + 1):
        pow2[i] = (pow2[i-1] * 2) % MOD
    
    # For each m from 1 to n
    for m in range(1, n + 1):
        total = 0
        
        # Consider all pairs (i, j) where 0 <= i < j < m (0-indexed)
        for i in range(m):
            for j in range(i + 1, m):
                g = gcd(a[i], a[j])
                # Number of subsequences where a[i] and a[j] are adjacent
                # = 2^(i) * 2^(m-j-1)
                count = (pow2[i] * pow2[m - j - 1]) % MOD
                total = (total + g * count) % MOD
        
        print(total)

solve()
