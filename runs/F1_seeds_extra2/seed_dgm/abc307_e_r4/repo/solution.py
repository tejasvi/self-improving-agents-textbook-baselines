import sys


def main():
    MOD = 998244353
    data = sys.stdin.read().split()
    N = int(data[0])
    M = int(data[1])
    # Chromatic polynomial of cycle C_N evaluated at M:
    # (M-1)^N + (-1)^N * (M-1)
    sign = 1 if N % 2 == 0 else MOD - 1
    ans = (pow(M - 1, N, MOD) + sign * (M - 1)) % MOD
    print(ans)


main()
