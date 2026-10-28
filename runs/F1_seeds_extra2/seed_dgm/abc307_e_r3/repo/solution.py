import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    mod = 998244353
    # Number of proper colorings of cycle C_n with m colors:
    # (m-1)^n + (-1)^n * (m-1)
    k = (m - 1) % mod
    res = pow(k, n, mod)
    if n % 2 == 0:
        res = (res + k) % mod
    else:
        res = (res - k) % mod
    print(res % mod)


if __name__ == "__main__":
    main()
