MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular inverse using Fermat's little theorem"""
    return pow(a, m - 2, m)

def solve(N, K):
    """
    Key insight: Due to symmetry, after enough operations, the expected position
    converges. But we can compute it directly using probability distributions.
    
    Let p[i] = probability that black ball is at position i after k operations
    Initial: p[1] = 1, p[i] = 0 for i > 1
    
    Transition:
    - P(black ball stays at position i) = 1 - 2(N-1)/N²
    - P(black ball moves from i to j, j≠i) = 2/N²
    """
    
    # Work with fractions mod MOD
    # Represent probability distribution as list of numerators (denominators implicit)
    
    # Current probability distribution: p[i] is the probability black ball is at position i
    # We'll compute this as integers mod MOD (with implicit denominator)
    
    # Transition matrix approach might be too slow for large N
    # Better approach: By symmetry, after enough time, all positions have equal probability
    # But for small K, we need exact computation
    
    # Use dynamic programming on positions
    # p[k][i] = probability black ball is at position i after k operations
    
    # But N can be up to 998244352, so we can't store full arrays
    # Key observation: Due to symmetry, we only need to track position 1 separately
    # All other positions have the same probability by symmetry
    
    # Let q[k] = probability black ball is at position 1 after k operations
    # By symmetry, probability of being at any position i > 1 is (1 - q[k]) / (N - 1)
    
    # Transition for position 1:
    # From position 1: stays with prob 1 - 2(N-1)/N², moves to any j>1 with prob 2/N²
    # From position i>1: stays with prob 1 - 2(N-1)/N², moves to 1 with prob 2/N²
    
    # q[k+1] = q[k] * (1 - 2(N-1)/N²) + (1 - q[k]) * (2/N²)
    #        = q[k] * (1 - 2(N-1)/N²) + 2/N² - q[k] * 2/N²
    #        = q[k] * (1 - 2(N-1)/N² - 2/N²) + 2/N²
    #        = q[k] * (1 - 2N/N²) + 2/N²
    #        = q[k] * (1 - 2/N) + 2/N²
    #        = q[k] * (N - 2)/N + 2/N²
    
    # Convert to modular arithmetic
    N_inv = modinv(N)
    N_inv_sq = (N_inv * N_inv) % MOD
    
    # q[0] = 1 (black ball starts at position 1)
    q = 1
    
    for _ in range(K):
        # q = q * (N - 2) / N + 2 / N²
        q = (q * (N - 2) % MOD * N_inv % MOD + 2 * N_inv_sq % MOD) % MOD
    
    # Expected position = q[K] * 1 + (1 - q[K]) / (N - 1) * (2 + 3 + ... + N)
    # where sum from 2 to N = (sum from 1 to N) - 1 = N(N+1)/2 - 1
    
    # E[X] = 1 * q + sum_{i=2}^{N} i * (1-q)/(N-1)
    #      = q + (1-q)/(N-1) * sum_{i=2}^{N} i
    #      = q + (1-q)/(N-1) * (N(N+1)/2 - 1)
    
    sum_pos = (N * (N + 1) // 2 - 1) % MOD
    
    # Actually let me recalculate more carefully
    # sum from i=2 to N = 2 + 3 + ... + N = (sum 1 to N) - 1 = N(N+1)/2 - 1
    
    # But with modular arithmetic:
    sum_pos = (N % MOD * ((N + 1) % MOD) % MOD * modinv(2) % MOD - 1 + MOD) % MOD
    
    # E[X] = q * 1 + (1 - q) * sum_pos / (N - 1)
    #      = q + (1 - q) * sum_pos * (N - 1)^{-1}
    
    one_minus_q = (1 - q + MOD) % MOD
    N_minus_1_inv = modinv(N - 1)
    
    expected = (q + one_minus_q * sum_pos % MOD * N_minus_1_inv % MOD) % MOD
    
    return expected

# Read input
N, K = map(int, input().split())
print(solve(N, K))
