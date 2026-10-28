# Solution for Random Walk on Tree problem
# Computes expected number of operations modulo 998244353 using derived formula.

import sys

def solve():
    MOD = 998244353
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])
    # Compute components modulo MOD
    inv6 = pow(6, MOD - 2, MOD)
    N_mod = N % MOD
    M_mod = M % MOD
    M1_mod = (M_mod + 1) % MOD
    # term = N * M * (M+1) * (M*(3N - 2) + 2) / 6  (mod MOD)
    threeN_mod = (3 * N_mod) % MOD
    inner = (M_mod * ((threeN_mod - 2) % MOD) + 2) % MOD
    term = N_mod * M_mod % MOD
    term = term * M1_mod % MOD
    term = term * inner % MOD
    ans = term * inv6 % MOD
    print(ans)

if __name__ == "__main__":
    solve()
