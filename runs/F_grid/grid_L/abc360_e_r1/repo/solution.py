import sys

MOD = 998244353


def main():
    N, K = map(int, sys.stdin.read().split())
    inv_n = pow(N, MOD - 2, MOD)
    # p = P(black ball at position 1) after K steps.
    # p_{k+1} = ((N-2)/N) p_k + 2/N^2, p_0 = 1, fixed point 1/N.
    r = (N - 2) * inv_n % MOD
    p = (inv_n + (1 - inv_n) * pow(r, K, MOD)) % MOD
    # E[x] = p + (1-p) * (N+2)/2  (other positions symmetric)
    half = pow(2, MOD - 2, MOD)
    ans = (p + (1 - p) * ((N + 2) % MOD) % MOD * half) % MOD
    print(ans)


if __name__ == "__main__":
    main()
