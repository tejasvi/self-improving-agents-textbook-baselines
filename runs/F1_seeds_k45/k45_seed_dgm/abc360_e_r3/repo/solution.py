MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular inverse of a modulo m using Fermat's little theorem"""
    return pow(a, m - 2, m)

def solve(N, K):
    # Key insight: By symmetry, after each operation, the probability that the black
    # ball is at any non-position-1 location should be equal.
    # 
    # Let p1[k] = probability that black ball is at position 1 after k operations
    # Then p_i[k] = (1 - p1[k]) / (N - 1) for any i != 1
    #
    # Transition probability:
    # - If black ball is at position 1, it moves to position j (j != 1) with prob 2/N²
    # - If black ball is at position j (j != 1), it moves to position 1 with prob 2/N²
    # - Otherwise it stays at its current position
    #
    # This gives us the recurrence:
    # p1[k+1] = p1[k] * (1 - 2(N-1)/N²) + (1 - p1[k]) * 2/N²
    #         = p1[k] * (N² - 2N) / N² + 2/N²
    #
    # This is a linear recurrence with solution:
    # p1[k] = a^k * ((N-1)/N) + 1/N
    # where a = (N² - 2N) / N²
    
    N_mod = N % MOD
    N_sq = (N_mod * N_mod) % MOD
    N_inv = modinv(N_mod)
    N_sq_inv = modinv(N_sq)
    
    # Coefficient a = (N² - 2N) / N² = (N - 2) / N
    # Actually: a = (N² - 2N) / N² = N(N - 2) / N² = (N - 2) / N
    a_num = (N_mod - 2 + MOD) % MOD
    a = (a_num * N_inv) % MOD
    
    # Compute a^K mod MOD
    a_pow_k = pow(a, K, MOD)
    
    # p1[K] = a^K * (N-1)/N + 1/N
    coeff = ((N_mod - 1 + MOD) * N_inv) % MOD
    p1 = (a_pow_k * coeff + N_inv) % MOD
    
    # Expected position:
    # E[x] = 1 * p1[K] + sum_{i=2}^{N} i * (1 - p1[K]) / (N - 1)
    #      = p1[K] + (1 - p1[K]) * (sum_{i=2}^{N} i) / (N - 1)
    #      = p1[K] + (1 - p1[K]) * (N+2) / 2
    
    one_minus_p1 = (1 - p1 + MOD) % MOD
    
    # (N + 2) / 2
    n_plus_2_div_2 = ((N_mod + 2) * modinv(2)) % MOD
    
    expected = (p1 + one_minus_p1 * n_plus_2_div_2) % MOD
    
    return expected

# Read input
N, K = map(int, input().split())

# Solve and print result
print(solve(N, K))
