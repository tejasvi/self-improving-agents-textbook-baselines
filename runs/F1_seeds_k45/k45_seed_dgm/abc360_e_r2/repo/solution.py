MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular inverse using Fermat's little theorem"""
    return pow(a, m - 2, m)

def solve(N, K):
    """
    Using eigenvalue analysis of the transition matrix.
    The black ball position follows:
    - p_k(0) = 1/N + (N-1)/N * ((N-2)/N)^k
    - p_k(i) = 1/N - 1/N * ((N-2)/N)^k for i > 0
    """
    
    if N == 1:
        return 1
    
    N_mod = N % MOD
    N_inv = modinv(N_mod)
    
    # Compute ((N-2)/N)^K mod MOD
    # This is ((N-2) * inv(N))^K
    base = ((N_mod - 2 + MOD) % MOD) * N_inv % MOD
    power = pow(base, K, MOD)
    
    # p_0(0) = 1/N + (N-1)/N * power
    p0 = (N_inv + (N_mod - 1) % MOD * N_inv % MOD * power) % MOD
    
    # p_0(i) = 1/N - 1/N * power for i > 0
    pi = (N_inv - N_inv * power % MOD + MOD) % MOD
    
    # Expected value = 1 * p_0(0) + sum_{i=1}^{N-1} (i+1) * p_0(i)
    # = 1 * p_0(0) + (2 + 3 + ... + N) * p_0(i) for i > 0 (all equal)
    # = 1 * p_0(0) + sum_{i=2}^{N} i * p_0(i-1)
    
    # Actually, expected = sum_{i=0}^{N-1} (i+1) * p(i)
    # = 1 * p(0) + sum_{i=1}^{N-1} (i+1) * p(i)
    # = 1 * p(0) + sum_{i=1}^{N-1} (i+1) * pi
    # = 1 * p(0) + pi * (2 + 3 + ... + N)
    # = 1 * p(0) + pi * (sum_{i=1}^{N} i - 1)
    # = 1 * p(0) + pi * (N*(N+1)/2 - 1)
    
    # sum_{i=1}^{N} i = N*(N+1)/2
    sum_2_to_N = (N_mod * (N_mod + 1) % MOD * modinv(2) - 1 + MOD) % MOD
    
    expected = (1 * p0 + pi * sum_2_to_N) % MOD
    
    return expected

# Read input
N, K = map(int, input().split())

# Solve and print answer
print(solve(N, K))
