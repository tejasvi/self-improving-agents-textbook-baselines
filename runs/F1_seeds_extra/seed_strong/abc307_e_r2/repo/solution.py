import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    # Chromatic polynomial of cycle C_n evaluated at m:
    # (m-1)^n + (-1)^n * (m-1)
    k = m - 1
    ans = pow(k, n, MOD)
    if n % 2 == 0:
        ans = (ans + k) % MOD
    else:
        ans = (ans - k) % MOD
    print(ans % MOD)


if __name__ == "__main__":
    main()
