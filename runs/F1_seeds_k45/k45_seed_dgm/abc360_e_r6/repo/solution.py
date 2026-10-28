MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular inverse using Fermat's little theorem"""
    return pow(a, m - 2, m)

def solve(N, K):
    # Let p_k = probability black ball is at its original position (1) after k operations
    # Let q_k = probability black ball is at any specific other position after k operations
    # Then: p_k + (N-1)*q_k = 1
    
    # Transition probabilities per operation:
    # If at position j: stays with prob (N²-2N+2)/N², moves to any other with prob 2/N²
    
    # p_{k+1} = p_k * (N²-2N+2)/N² + (N-1) * q_k * 2/N²
    # Since q_k = (1 - p_k) / (N-1):
    # p_{k+1} = p_k * (N²-2N+2)/N² + (1-p_k) * 2/N²
    #         = p_k * [(N²-2N+2) - 2]/N² + 2/N²
    #         = p_k * (N²-2N)/N² + 2/N²
    #         = p_k * (N-2)/N + 2/N²
    
    p = 1  # p_0 = 1, ball starts at position 1
    
    N_mod = N % MOD
    N_inv = modinv(N_mod)
    N_sq_inv = (N_inv * N_inv) % MOD
    
    for _ in range(K):
        # p_new = p * (N-2)/N + 2/N²
        term1 = (p * ((N_mod - 2 + MOD) % MOD) % MOD * N_inv) % MOD
        term2 = (2 * N_sq_inv) % MOD
        p = (term1 + term2) % MOD
    
    # p = P(at position 1 after K ops)
    # For each other position i (2 to N): P(at position i) = (1-p)/(N-1)
    
    # E = 1 * p + sum(i * (1-p)/(N-1)) for i in 2..N
    #   = p + (1-p)/(N-1) * sum(i for i in 2..N)
    #   = p + (1-p)/(N-1) * (2+3+...+N)
    #   = p + (1-p)/(N-1) * (N*(N+1)/2 - 1)
    
    one_minus_p = (1 - p + MOD) % MOD
    
    # sum(i for i in 2..N) = N*(N+1)/2 - 1
    N_mod = N % MOD
    sum_other = (N_mod * ((N_mod + 1) % MOD) % MOD * modinv(2) % MOD - 1 + MOD) % MOD
    
    # E = p + one_minus_p * sum_other / (N-1)
    N_minus_1_inv = modinv((N - 1) % MOD)
    contribution_from_others = (one_minus_p * sum_other % MOD * N_minus_1_inv) % MOD
    
    E = (p + contribution_from_others) % MOD
    
    return E

N, K = map(int, input().split())
print(solve(N, K))
