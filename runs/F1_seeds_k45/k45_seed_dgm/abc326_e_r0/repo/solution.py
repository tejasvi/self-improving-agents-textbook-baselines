MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular inverse using Fermat's little theorem"""
    return pow(a, m - 2, m)

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    # E[i] = expected salary when starting from state x=i (0-indexed, so E[i] is for state i+1)
    # E[i] = (1/N) * sum(A[j] + E[j] for j in range(i+1, N))
    # where indices are 0-based
    
    # Let's work backwards from state N-1
    E = [0] * N  # E[i] represents expected salary starting from state i+1 (1-indexed)
    
    # Base case: E[N-1] = 0 (at state N, we can only roll 1..N, all <= N, so we terminate)
    E[N - 1] = 0
    
    inv_N = modinv(N)
    
    # Work backwards
    for i in range(N - 2, -1, -1):
        # E[i] = (1/N) * sum(A[j] + E[j] for j in range(i+1, N))
        # Indices: i is for state i+1 (0-indexed A and E)
        total = 0
        for j in range(i + 1, N):
            total = (total + A[j] + E[j]) % MOD
        E[i] = (inv_N * total) % MOD
    
    # We need E for state 0 (starting state)
    # When at state 0, rolling gives us j from 1 to N (all > 0)
    # So expected = (1/N) * sum(A[j-1] + E[j-1] for j in range(1, N+1))
    #            = (1/N) * sum(A[j] + E[j] for j in range(N))
    
    total = 0
    for j in range(N):
        total = (total + A[j] + E[j]) % MOD
    
    result = (inv_N * total) % MOD
    print(result)

solve()
