MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular inverse of a modulo m using Fermat's little theorem"""
    return pow(a, m - 2, m)

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    # E[i] represents the expected salary starting from state x=i
    # We work backwards from i=N-1 to i=0
    
    E = [0] * (N + 1)
    inv_N = modinv(N)
    
    # E[N] = 0 (no roll can give j > N)
    E[N] = 0
    
    # Calculate E[i] for i from N-1 down to 0
    for i in range(N - 1, -1, -1):
        # E[i] = (1/N) * sum(A[j] + E[j] for j in range(i+1, N))
        # In 0-indexed: A[j-1] + E[j] for j in range(i+1, N+1)
        total = 0
        for j in range(i + 1, N + 1):
            # When we roll j (1-indexed), we get A[j-1] (0-indexed)
            total = (total + A[j - 1] + E[j]) % MOD
        
        E[i] = (total * inv_N) % MOD
    
    return E[0]

print(solve())
