import sys

MOD = 998244353


def main():
    N, K = map(int, sys.stdin.read().split())
    inv_n = pow(N, MOD - 2, MOD)
    # E_{k+1} = (1 - 2/N) E_k + (N+1)/N, E_0 = 1, fixed point (N+1)/2
    c = (1 - 2 * inv_n) % MOD
    # Closed form: E_K = (N+1)/2 + c^K * (1 - (N+1)/2)
    half = (N + 1) * pow(2, MOD - 2, MOD) % MOD
    ans = (half + pow(c, K, MOD) * ((1 - half) % MOD)) % MOD
    print(ans)


main()
