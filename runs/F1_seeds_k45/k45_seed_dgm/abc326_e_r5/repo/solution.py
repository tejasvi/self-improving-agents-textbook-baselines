MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular inverse using Fermat's little theorem"""
    return pow(a, m - 2, m)

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    # E[i] = expected salary starting from state x=i (0-indexed, so A[i] is for position i+1)
    # We need E[0]
    
    # For state i (0-indexed), when we roll:
    # - With probability 1/N, we get result j (1 to N, which is indices 0 to N-1)
    # - If j > i: we get A[j-1] + E[j] (converting to 0-indexed)
    # - If j <= i: we terminate
    
    # Let's work backwards from position N
    E = [0] * (N + 1)  # E[i] is expected salary from state i
    
    # E[N] = 0 because there's no outcome > N
    
    # For i from N-1 down to 0:
    # E[i] = (1/N) * sum(A[j] + E[j+1] for j in range(i, N))
    # Multiply by N: N*E[i] = sum(A[j] + E[j+1] for j in range(i, N))
    
    inv_N = modinv(N)
    
    for i in range(N - 1, -1, -1):
        total = 0
        for j in range(i, N):
            # We roll j+1 (since j is 0-indexed)
            # We get A[j] and then continue from state j+1
            total = (total + A[j] + E[j + 1]) % MOD
        
        E[i] = (total * inv_N) % MOD
    
    return E[0]

print(solve())
