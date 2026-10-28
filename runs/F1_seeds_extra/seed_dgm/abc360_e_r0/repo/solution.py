import sys

MOD = 998244353


def main():
    N, K = map(int, sys.stdin.read().split())
    inv = lambda x: pow(x % MOD, MOD - 2, MOD)
    invN = inv(N)
    # p_k = probability black ball is at position 1
    # p_{k+1} = p_k * (1 - 2/N) + (1 - p_k) * ... ; closed form:
    # p_K = 1/N + (1 - 1/N) * (1 - 2/N)^K
    r = (1 - 2 * invN) % MOD
    p = (invN + (1 - invN) % MOD * pow(r, K, MOD)) % MOD
    # Other positions are symmetric: E = p + (1-p) * (N+2)/2
    half = inv(2)
    ans = (p + (1 - p) % MOD * ((N + 2) % MOD) % MOD * half) % MOD
    print(ans)


if __name__ == "__main__":
    main()
