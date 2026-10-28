import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    k = (m - 1) % MOD
    res = pow(k, n, MOD)
    if n % 2 == 0:
        res = (res + k) % MOD
    else:
        res = (res - k) % MOD
    print(res)

main()
