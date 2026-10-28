import sys

MOD = 998244353


def main():
    N, K = map(int, sys.stdin.read().split())
    if N == 1:
        print(1)
        return
    inv_n = pow(N, MOD - 2, MOD)
    # q_k = P(black ball at position 1) after k operations
    # q_k = 1/N + (1 - 1/N) * (1 - 2/N)^k
    r = (1 - 2 * inv_n) % MOD
    q = (inv_n + (1 - inv_n) % MOD * pow(r, K, MOD)) % MOD
    # Other positions are symmetric: each has probability (1-q)/(N-1),
    # and the average of positions 2..N is (N+2)/2.
    half_avg = (N + 2) * pow(2, MOD - 2, MOD) % MOD
    ans = (q + (1 - q) * half_avg) % MOD
    print(ans)


if __name__ == "__main__":
    main()
