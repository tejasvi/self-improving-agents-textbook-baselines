import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    K = int(data[1])
    inv_n = pow(N, MOD - 2, MOD)
    # p_k = probability black ball is at position 1 after k operations
    # p_{k+1} = p_k * (1 - 2/N) + 2/N^2 ; fixed point 1/N
    # p_k = 1/N + (1 - 1/N) * (1 - 2/N)^k
    r = (1 - 2 * inv_n) % MOD
    p = (inv_n + (1 - inv_n) % MOD * pow(r, K, MOD)) % MOD
    # E[x] = p * 1 + (1 - p) * (average of positions 2..N) = p + (1 - p) * (N + 2) / 2
    half = pow(2, MOD - 2, MOD)
    ans = (p + (1 - p) % MOD * ((N + 2) % MOD) % MOD * half) % MOD
    print(ans)


if __name__ == "__main__":
    main()
