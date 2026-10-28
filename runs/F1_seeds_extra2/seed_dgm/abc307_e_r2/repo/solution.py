import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    # Number of proper colorings of cycle C_n with m colors:
    # (m-1)^n + (-1)^n * (m-1)
    t = pow(m - 1, n, MOD)
    if n % 2 == 0:
        ans = (t + (m - 1)) % MOD
    else:
        ans = (t - (m - 1)) % MOD
    print(ans)


main()
