from math import gcd

MOD = 998244353

N = int(input())
A = list(map(int, input().split()))

# Precompute powers of 2
pow2 = [1] * N
for i in range(1, N):
    pow2[i] = (pow2[i-1] * 2) % MOD

answer = 0
for m in range(N):
    # When adding A[m], we form pairs (A[i], A[m]) for all i < m
    # Each pair (A[i], A[m]) contributes gcd(A[i], A[m]) * 2^i * 2^(m-m-1) = gcd(A[i], A[m]) * 2^i
    
    for i in range(m):
        g = gcd(A[i], A[m])
        contribution = (g * pow2[i]) % MOD
        answer = (answer + contribution) % MOD
    
    print(answer)
