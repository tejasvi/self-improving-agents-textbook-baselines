MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular inverse using Fermat's little theorem"""
    return pow(a, m - 2, m)

def solve(N, K):
    # Due to symmetry, we only need to track:
    # p1 = probability that black ball is at position 1
    # p_rest = probability that black ball is at any other specific position
    # (all other positions have the same probability)
    
    # Initially: p1 = 1, p_rest = 0
    
    # Transition:
    # Position 1:
    # - From position 1: prob_stay = (N^2 - 2N + 2) / N^2
    # - From any other position (N-1 positions): prob_move / (N-1) = 2 / (N^2 * (N-1))
    # Actually, from position j (j != 1) to position 1: prob_move = 2 / N^2
    # So new_p1 = p1 * prob_stay / N^2 + (1 - p1) * (2 / N^2)
    #           = p1 * prob_stay / N^2 + (2 - 2*p1) / N^2
    #           = (p1 * prob_stay + 2 - 2*p1) / N^2
    
    # Position k (k != 1):
    # - From position k: prob_stay / (N-1) [NO! Each position stays with prob_stay/N^2]
    # - Actually, new_p_rest comes from:
    #   * Position 1 moving to position k: p1 * 2 / N^2
    #   * Position k staying: p_rest * prob_stay / N^2
    #   * Any other position (N-2 others) moving to position k: p_rest * 2 / N^2
    # So new_p_rest = p1 * (2/N^2) + p_rest * prob_stay / N^2 + (N-2) * p_rest * (2/N^2)
    #               = p1 * (2/N^2) + p_rest * (prob_stay + 2*(N-2)) / N^2
    
    # Let's verify: total = p1 + (N-1) * p_rest should remain 1
    # new_p1 + (N-1) * new_p_rest
    # = (p1*prob_stay + 2 - 2*p1)/N^2 + (N-1)*(p1*2 + p_rest*(prob_stay + 2*N - 4))/N^2
    # = (p1*prob_stay + 2 - 2*p1 + (N-1)*p1*2 + (N-1)*p_rest*(prob_stay + 2*N - 4))/N^2
    # = (p1*(prob_stay - 2 + 2*N - 2) + 2 + (N-1)*p_rest*(prob_stay + 2*N - 4))/N^2
    # = (p1*(N^2 - 2N + 2 + 2N - 4) + 2 + (N-1)*p_rest*(prob_stay + 2*N - 4))/N^2
    # = (p1*(N^2 - 2) + 2 + (N-1)*p_rest*(prob_stay + 2*N - 4))/N^2
    
    # Hmm, this is getting complicated. Let me recalculate.
    
    # Actually, let's just compute it directly for the general case:
    # new_p_k = sum over all j of (p_j * P(j -> k))
    # where P(j -> k) = prob_stay / N^2 if j = k, else 2 / N^2
    
    # For k = 1:
    # new_p1 = p1 * prob_stay/N^2 + sum over j!=1 (p_j * 2/N^2)
    #        = p1 * prob_stay/N^2 + (1 - p1) * 2/N^2
    
    # For k != 1:
    # new_p_rest = p1 * 2/N^2 + p_rest * prob_stay/N^2 + sum over j!=1,j!=k (p_j * 2/N^2)
    #            = p1 * 2/N^2 + p_rest * prob_stay/N^2 + (1 - p1 - p_rest) * 2/N^2
    #            = p1 * 2/N^2 + p_rest * prob_stay/N^2 + 2/N^2 - 2*p1/N^2 - 2*p_rest/N^2
    #            = p_rest * (prob_stay - 2)/N^2 + 2/N^2 - 2*p1/N^2 + 2*p1/N^2
    #            = p_rest * (prob_stay - 2)/N^2 + 2/N^2
    
    # Wait, that doesn't look right either. Let me reconsider.
    
    # p_rest should represent the probability of being at any ONE of the other N-1 positions
    # Total probability = p1 + (N-1) * p_rest = 1
    
    # For position k (k != 1), there are N-1 such positions.
    # new_p_rest = p1 * 2/N^2 + p_rest * prob_stay/N^2 + (N-2) * p_rest * 2/N^2
    #            = p1 * 2/N^2 + p_rest * (prob_stay + 2*(N-2))/N^2
    #            = p1 * 2/N^2 + p_rest * (prob_stay + 2*N - 4)/N^2
    
    # And prob_stay = N^2 - 2N + 2
    # So: new_p_rest = (p1 * 2 + p_rest * (N^2 - 2N + 2 + 2*N - 4))/N^2
    #                = (p1 * 2 + p_rest * (N^2 - 2))/N^2
    
    # For position 1:
    # new_p1 = p1 * prob_stay/N^2 + (N-1)*p_rest * 2/N^2
    #        = (p1 * (N^2 - 2N + 2) + 2*(N-1)*p_rest)/N^2
    
    # Verify: new_p1 + (N-1)*new_p_rest
    # = (p1*(N^2-2N+2) + 2*(N-1)*p_rest + (N-1)*(p1*2 + p_rest*(N^2-2)))/N^2
    # = (p1*(N^2-2N+2+2*N-2) + p_rest*(2*N-2+N^2-2))/N^2
    # = (p1*N^2 + p_rest*N^2)/N^2
    # Since p1 + (N-1)*p_rest = 1, we have p1*N^2 + p_rest*N^2*(N-1) should equal N^2
    # Actually, p1 + (N-1)*p_rest = 1, so p1 = 1 - (N-1)*p_rest
    # Then: (1 - (N-1)*p_rest)*N^2 + (N-1)*p_rest*N^2 = N^2 ✓
    
    prob_stay = (N * N - 2 * N + 2) % MOD
    inv_n2 = modinv((N * N) % MOD)
    
    p1 = 1
    p_rest = 0
    
    for _ in range(K):
        # new_p1 = (p1 * prob_stay + 2 * (N-1) * p_rest) * inv_n2
        # new_p_rest = (p1 * 2 + p_rest * (N^2 - 2)) * inv_n2
        
        new_p1 = (p1 * prob_stay % MOD + 2 * (N - 1) % MOD * p_rest % MOD) % MOD
        new_p1 = new_p1 * inv_n2 % MOD
        
        new_p_rest = (p1 * 2 % MOD + p_rest * ((N * N - 2) % MOD) % MOD) % MOD
        new_p_rest = new_p_rest * inv_n2 % MOD
        
        p1 = new_p1
        p_rest = new_p_rest
    
    # Expected position = 1 * p1 + sum over k=2 to N of (k * p_rest)
    # = p1 + p_rest * (2 + 3 + ... + N)
    # = p1 + p_rest * (sum from 1 to N minus 1)
    # = p1 + p_rest * (N*(N+1)/2 - 1)
    
    sum_2_to_N = (N * (N + 1) // 2 - 1) % MOD
    expected = (p1 + p_rest * sum_2_to_N % MOD) % MOD
    
    return expected

# Read input
N, K = map(int, input().split())
print(solve(N, K))
