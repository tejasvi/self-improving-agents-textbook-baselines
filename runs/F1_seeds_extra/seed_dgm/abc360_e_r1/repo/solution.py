import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    K = int(data[1])
    if N == 1:
        print(1)
        return
    invN = pow(N, MOD - 2, MOD)
    inv2 = pow(2, MOD - 2, MOD)
    # p: probability black ball is at position 1
    # p' = p*(1 - 2/N) + 2/N^2 * (1 - p) ... simplified below
    # Derived: p' = p*(1 - 2/N) + 2/N^2
    a = (1 - 2 * invN) % MOD
    b = 2 * invN % MOD * invN % MOD
    p = 1
    for _ in range(K):
        p = (p * a + b) % MOD
    # E = p + (1 - p) * (N + 2) / 2
    ans = (p + (1 - p) % MOD * ((N + 2) % MOD) % MOD * inv2) % MOD
    print(ans)


if __name__ == "__main__":
    main()
