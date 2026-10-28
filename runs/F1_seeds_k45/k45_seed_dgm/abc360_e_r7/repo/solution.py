MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular inverse of a mod m using Fermat's little theorem"""
    return pow(a, m - 2, m)

def solve(N, K):
    if N == 1:
        # Special case: only one ball, it's always at position 1
        return 1
    
    # Let q(k) be the probability that the black ball is at position 1 after k operations
    # By symmetry, for i > 1, P(position i) = (1 - q(k)) / (N - 1)
    
    # Recurrence: q(k+1) = q(k) * (N - 2) / N + 2 / N^2
    
    q = 1  # q(0) = 1, black ball starts at position 1
    inv_n = modinv(N, MOD)
    inv_n_sq = modinv(N * N % MOD, MOD)
    
    for _ in range(K):
        # q(k+1) = q(k) * (N - 2) / N + 2 / N^2
        q = (q * (N - 2) % MOD * inv_n % MOD + 2 * inv_n_sq) % MOD
    
    # Expected position = (-q(k) * N + N + 2) / 2
    # = (N + 2 - q(k) * N) / 2
    
    inv_2 = modinv(2, MOD)
    numerator = (N + 2 - q * N % MOD) % MOD
    expected = numerator * inv_2 % MOD
    
    return expected

# Read input
N, K = map(int, input().split())

# Solve and print result
print(solve(N, K))
