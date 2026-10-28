MOD = 998244353

def modinv(a):
    return pow(a, MOD - 2, MOD)

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    # E[i] = expected salary starting from state x=i
    # E[i] = (1/N) * sum(A[j] + E[j] for j in range(i+1, N))
    # where A is 0-indexed, so A[j] is the j+1-th element
    
    # Work backwards: E[N-1] = 0, then compute E[i] for i from N-2 down to -1
    # (where -1 corresponds to initial state x=0)
    
    # E[i] = (1/N) * sum((A[j] + E[j]) for j > i)
    # Let's compute suffix sums to make this efficient
    
    E = [0] * (N + 1)  # E[0] to E[N], where E[N] = 0
    
    inv_N = modinv(N)
    
    # Work backwards from i = N-1 to i = -1 (initial state)
    # But we'll shift indices: let's compute E directly
    
    # E[i] represents expected salary when starting from position i (1-indexed)
    # E[0] represents initial state (x=0)
    
    for i in range(N - 1, -1, -1):
        # E[i] = (1/N) * sum(A[j] + E[j+1] for j = i to N-1)
        total = 0
        for j in range(i, N):
            total = (total + A[j] + E[j + 1]) % MOD
        E[i] = (total * inv_N) % MOD
    
    return E[0]

print(solve())
