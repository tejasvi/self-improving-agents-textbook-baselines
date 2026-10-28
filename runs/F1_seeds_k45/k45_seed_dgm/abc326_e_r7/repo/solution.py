MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular inverse of a modulo m using Fermat's little theorem."""
    return pow(a, m - 2, m)

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    # E[i] = expected salary starting from state x=i
    # E[i] = (1/N) * sum(A[j] + E[j] for j in range(i+1, N))
    # where A is 0-indexed, so A[j] is the (j+1)-th element
    
    E = [0] * (N + 1)  # E[N] = 0 (boundary condition)
    
    inv_N = modinv(N)
    
    # Work backwards from state N to 0
    for i in range(N - 1, -1, -1):
        # E[i] = (1/N) * sum(A[j] + E[j+1] for j in range(i, N))
        # Note: A is 0-indexed, A[j] corresponds to rolling (j+1)
        # If we're at state i and roll (j+1), we move to state j+1
        
        total = 0
        for j in range(i, N):
            # Rolling (j+1) gives us A[j] and moves us to state j+1
            total = (total + A[j] + E[j + 1]) % MOD
        
        E[i] = (total * inv_N) % MOD
    
    print(E[0])

solve()
