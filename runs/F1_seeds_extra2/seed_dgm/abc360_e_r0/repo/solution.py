import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    K = int(data[1])

    # p = probability the black ball is at position 1.
    # Other positions are symmetric, so each has probability (1-p)/(N-1).
    # Expected x = p + (1-p) * (N+2)/2.
    inv_n2 = pow(N * N % MOD, MOD - 2, MOD)
    stay = (1 - 2 * (N - 1) % MOD * inv_n2) % MOD  # prob stay at 1 given at 1
    come = 2 * inv_n2 % MOD                        # prob move to 1 from a specific other spot

    p = 1
    for _ in range(K):
        p = (p * stay + (1 - p) * come) % MOD

    half_shift = (N + 2) * pow(2, MOD - 2, MOD) % MOD
    ans = (p + (1 - p) * half_shift) % MOD
    print(ans)


if __name__ == "__main__":
    main()
