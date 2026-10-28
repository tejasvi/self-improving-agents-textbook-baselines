# Solution for Random Walk on Tree problem.
import sys
MOD = 998244353

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])
    inv2 = pow(2, MOD - 2, MOD)
    inv6 = pow(6, MOD - 2, MOD)
    V = N * M + 1  # total vertices
    # Compute S1 = M*(M+1)/2  (mod)
    M_mod = M % MOD
    S1 = M_mod * ((M + 1) % MOD) % MOD * inv2 % MOD
    # Compute S2 = M*(M+1)*(2M+1)/6  (mod)
    S2 = M_mod * ((M + 1) % MOD) % MOD * ((2 * M_mod + 1) % MOD) % MOD * inv6 % MOD
    term = ( (V % MOD) * S1 - S2 ) % MOD
    ans = (N % MOD) * term % MOD
    print(ans)

if __name__ == "__main__":
    solve()
