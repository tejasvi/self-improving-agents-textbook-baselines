import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    MOD = 998244353
    k = (m - 1) % MOD
    ans = (pow(k, n, MOD) + (1 if n % 2 == 0 else -1) * k) % MOD
    print(ans)


if __name__ == "__main__":
    main()
