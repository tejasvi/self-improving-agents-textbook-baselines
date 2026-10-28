import math

MOD = 998244353

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    # Precompute powers of 2
    pow2 = [1] * (N + 1)
    for i in range(1, N + 1):
        pow2[i] = (pow2[i-1] * 2) % MOD
    
    # For each m from 1 to N
    for m in range(1, N + 1):
        total_score = 0
        
        # Consider all pairs (i, j) where i < j and both are in first m elements
        # These pairs contribute to the score
        for i in range(m):
            for j in range(i + 1, m):
                # The pair (A[i], A[j]) appears consecutively in subsequences
                # where all elements between them are excluded, but elements
                # before i and after j can be anything
                
                # Number of subsequences where i and j are consecutive:
                # - We must include i and j
                # - We can include/exclude elements before i: 2^i ways
                # - We can include/exclude elements after j within first m: 2^(m-j-1) ways
                # - We must exclude all elements between i and j: 1 way
                
                num_subseq = (pow2[i] * pow2[m - j - 1]) % MOD
                g = gcd(A[i], A[j])
                contribution = (num_subseq * g) % MOD
                total_score = (total_score + contribution) % MOD
        
        print(total_score)

solve()
