# Write your solution here. Read from stdin, write to stdout.

MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular inverse of a modulo m using Fermat's little theorem"""
    return pow(a, m - 2, m)

def solve():
    N, K = map(int, input().split())
    
    # p[j] = probability that black ball is at position j (1-indexed, but we use 0-indexed)
    # We'll use position 0 to N-1 internally
    p = [0] * N
    p[0] = 1  # Black ball starts at position 1 (index 0)
    
    # For each operation
    for _ in range(K):
        # new_p[j] = probability that black ball is at position j after this operation
        new_p = [0] * N
        
        # For each current position i where black ball might be
        for i in range(N):
            if p[i] == 0:
                continue
            
            # Probability that black ball stays at position i:
            # - We choose position i twice: 1/N²
            # - We choose i and some other position j: this causes swap, so it doesn't stay
            # So only way to stay is choose i twice: 1/N²
            
            stay_prob = 1 * modinv(N * N)  # 1/N²
            new_p[i] = (new_p[i] + p[i] * stay_prob) % MOD
            
            # Probability that black ball moves from i to j (j ≠ i):
            # We need to choose i and j (in any order): 2/N²
            for j in range(N):
                if i == j:
                    continue
                move_prob = 2 * modinv(N * N)  # 2/N²
                new_p[j] = (new_p[j] + p[i] * move_prob) % MOD
        
        p = new_p
    
    # Expected position (1-indexed) = sum of position * probability
    # Positions are 1, 2, ..., N (but we're using 0-indexed internally)
    expected = 0
    for i in range(N):
        expected = (expected + (i + 1) * p[i]) % MOD
    
    print(expected)

solve()
