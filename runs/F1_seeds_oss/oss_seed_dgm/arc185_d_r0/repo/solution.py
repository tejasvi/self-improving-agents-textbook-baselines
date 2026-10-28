# Solution for "Random Walk on Tree"
# The tree consists of N rays (branches) of length M each, attached to the root (vertex 0).
# Expected number of moves until all vertices are painted equals:
#   S = N * sum_{k=1}^{M} k * ( (N*M+1) - k )
#   = N * ( n * sum k - sum k^2 ) where n = N*M + 1
#   = N * ( n * M(M+1)/2 - M(M+1)(2M+1)/6 )
# The result is required modulo MOD = 998244353.

import sys
MOD = 998244353
INV2 = (MOD + 1) // 2          # modular inverse of 2 (since MOD is prime and MOD%2==1)
INV6 = pow(6, MOD - 2, MOD)    # modular inverse of 6

def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])

    N_mod = N % MOD
    M_mod = M % MOD
    n_mod = (N_mod * M_mod + 1) % MOD

    # term1 = n * M(M+1)/2  (mod MOD)
    term1 = n_mod * M_mod % MOD * ((M_mod + 1) % MOD) % MOD * INV2 % MOD

    # term2 = M(M+1)(2M+1)/6  (mod MOD)
    term2 = M_mod * ((M_mod + 1) % MOD) % MOD * ((2 * M_mod + 1) % MOD) % MOD * INV6 % MOD

    inner = (term1 - term2) % MOD
    answer = N_mod * inner % MOD
    print(answer)

if __name__ == "__main__":
    solve()
