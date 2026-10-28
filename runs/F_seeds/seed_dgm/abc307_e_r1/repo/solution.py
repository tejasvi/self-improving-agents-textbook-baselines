import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    # Number of proper colorings of cycle C_n with m colors:
    # (m-1)^n + (-1)^n * (m-1)
    k = (m - 1) % MOD
    sign = 1 if n % 2 == 0 else MOD - 1
    ans = (pow(k, n, MOD) + sign * k) % MOD
    print(ans)


if __name__ == "__main__":
    main()
