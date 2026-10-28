import sys

MOD = 998244353

def main():
    N, K = map(int, sys.stdin.read().split())
    inv_n = pow(N, MOD - 2, MOD)
    # p_k = P(black ball at position 1) = 1/N + (1 - 1/N) * (1 - 2/N)^K
    base = (1 - 2 * inv_n) % MOD
    p = (inv_n + (1 - inv_n) % MOD * pow(base, K, MOD)) % MOD
    # E[x] = p + (1 - p) * (N + 2) / 2
    inv2 = pow(2, MOD - 2, MOD)
    ans = (p + (1 - p) % MOD * ((N + 2) % MOD) % MOD * inv2) % MOD
    print(ans)

main()
