# Write your solution here. Read from stdin, write to stdout.

MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular inverse using Fermat's little theorem"""
    return pow(a, m - 2, m)

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    # E[i] = expected salary starting from state x=i
    # For state i: when we roll the die:
    # - With probability 1/N, we get j (1 <= j <= N)
    # - If j > i: we get A[j-1] and continue from state j
    # - If j <= i: we terminate
    # 
    # E[i] = (1/N) * sum(A[j-1] + E[j] for j in range(i+1, N+1))
    # N * E[i] = sum(A[j-1] + E[j] for j in range(i+1, N+1))
    # N * E[i] = sum(A[j-1] for j in range(i+1, N+1)) + sum(E[j] for j in range(i+1, N+1))
    
    # We work backwards from state N
    # E[N] = 0 (no more rolls can give j > N)
    
    E = [0] * (N + 1)  # E[0] to E[N], but we only use E[1] to E[N] and want E[0]
    
    # Work backwards from i = N-1 down to 0
    inv_N = modinv(N)
    
    for i in range(N - 1, -1, -1):
        # E[i] = (1/N) * sum(A[j-1] + E[j] for j in range(i+1, N+1))
        total = 0
        for j in range(i + 1, N + 1):
            total = (total + A[j - 1] + E[j]) % MOD
        E[i] = (total * inv_N) % MOD
    
    print(E[0])

solve()
