import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    # Chromatic polynomial of cycle C_n evaluated at m:
    # (m-1)^n + (-1)^n * (m-1)
    t = (m - 1) % MOD
    ans = pow(t, n, MOD)
    if n % 2 == 0:
        ans = (ans + t) % MOD
    else:
        ans = (ans - t) % MOD
    print(ans % MOD)


main()
