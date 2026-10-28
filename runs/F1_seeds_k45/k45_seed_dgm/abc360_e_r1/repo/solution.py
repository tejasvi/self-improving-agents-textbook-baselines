MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular inverse using Fermat's little theorem"""
    return pow(a, m - 2, m)

def solve(N, K):
    # We use a Markov chain approach with matrix exponentiation
    # The transition matrix has a special structure due to symmetry
    
    if N == 1:
        return 1
    
    # Transition probabilities (as fractions mod MOD):
    # P[i][i] = (N^2 - 2N + 2) / N^2
    # P[i][j] = 2 / N^2 for j != i
    
    # This can be rewritten as:
    # P = [(N^2 - 2N + 2) / N^2] * I + [2 / N^2] * (J - I)
    # where J is the all-ones matrix (all entries are 1)
    
    # The distribution after K steps can be computed using eigenvalue decomposition
    # For the initial state [1, 0, 0, ...]:
    # - Component along eigenvalue 1: converges to uniform (1/N for each state)
    # - Component along other eigenvalues decays
    
    N_sq = (N * N) % MOD
    N_sq_inv = modinv(N_sq)
    
    # Coefficients
    stay_coeff = (N * N - 2 * (N - 1)) % MOD
    stay_coeff = (stay_coeff * N_sq_inv) % MOD
    
    move_coeff = (2 * N_sq_inv) % MOD
    
    # For a symmetric transition matrix of this form:
    # After K steps, the probability distribution is:
    # p_i(K) = 1/N + (δ_{i,0} - 1/N) * λ^K
    # where λ = stay_coeff - (N-1) * move_coeff (the non-uniform eigenvalue)
    # and δ_{i,0} = 1 if i=0, 0 otherwise
    
    # λ = stay_coeff - (N-1) * move_coeff
    # = (N^2 - 2N + 2)/N^2 - (N-1) * 2/N^2
    # = (N^2 - 2N + 2 - 2N + 2) / N^2
    # = (N^2 - 4N + 4) / N^2
    # = (N-2)^2 / N^2
    
    lambda_num = ((N - 2) * (N - 2)) % MOD
    lambda_val = (lambda_num * N_sq_inv) % MOD
    
    # λ^K mod MOD
    lambda_k = pow(lambda_val, K, MOD)
    
    # For position 0 (the starting position):
    # p_0(K) = 1/N + (1 - 1/N) * λ^K
    #        = 1/N + ((N-1)/N) * λ^K
    
    # For position i (i != 0):
    # p_i(K) = 1/N + (0 - 1/N) * λ^K
    #        = 1/N - (1/N) * λ^K
    
    N_inv = modinv(N)
    
    p_0_after_k = (N_inv + ((N - 1) * N_inv % MOD) * lambda_k) % MOD
    p_i_after_k = (N_inv - N_inv * lambda_k) % MOD
    
    # Expected position = sum of (i+1) * p_i for i in [0, N-1]
    # = 1 * p_0 + 2 * p_1 + ... + N * p_{N-1}
    # = sum of (i+1) * [p_i]
    
    # We can split this:
    # E = 1 * p_0(K) + sum_{i=1}^{N-1} (i+1) * p_i(K)
    # = 1 * p_0(K) + sum_{i=1}^{N-1} (i+1) * [1/N - (1/N)*λ^K]
    # = p_0(K) + sum_{i=1}^{N-1} (i+1) * 1/N - sum_{i=1}^{N-1} (i+1) * (1/N)*λ^K
    
    # sum_{i=1}^{N-1} (i+1) = 2 + 3 + ... + N = (sum from 1 to N) - 1 = N(N+1)/2 - 1
    sum_positions_except_0 = (N * (N + 1) // 2 - 1) % MOD
    
    # Total sum of all positions * 1/N
    uniform_contribution = (sum_positions_except_0 * N_inv) % MOD
    
    # Decay contribution
    decay_coeff = (sum_positions_except_0 * N_inv % MOD) * lambda_k % MOD
    
    # But we need to account for position 0 separately
    expected = (p_0_after_k + uniform_contribution - decay_coeff) % MOD
    
    return expected

# Read input
N, K = map(int, input().split())

# Solve and print result
print(solve(N, K))
