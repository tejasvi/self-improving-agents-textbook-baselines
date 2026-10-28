import sys

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    MOD = 998244353
    x = (m - 1) % MOD
    sign = 1 if n % 2 == 0 else MOD - 1
    ans = (pow(x, n, MOD) + sign * x) % MOD
    print(ans)

main()
