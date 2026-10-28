import sys

MOD = 998244353


def main():
    N, K = map(int, sys.stdin.read().split())
    inv_n = pow(N, MOD - 2, MOD)
    # p_k = probability black ball is at position 1 after k operations.
    # p_{k+1} = p_k * (1 - 2/N) + 2/N^2, fixed point 1/N, p_0 = 1
    # => p_K = 1/N + (1 - 2/N)^K * (1 - 1/N)
    r = (1 - 2 * inv_n) % MOD
    p = (inv_n + pow(r, K, MOD) * (1 - inv_n)) % MOD
    # E[x] = p + (1 - p) * (N + 2) / 2
    half = pow(2, MOD - 2, MOD)
    ans = (p + (1 - p) * ((N + 2) % MOD) % MOD * half) % MOD
    print(ans)


if __name__ == "__main__":
    main()
