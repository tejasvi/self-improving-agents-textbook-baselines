import sys

def main():
    MOD = 998244353
    data = sys.stdin.read().split()
    N = int(data[0])
    M = int(data[1])
    # H_N = sum_{i=1}^N 1/i mod p
    h = 0
    for i in range(1, N + 1):
        h += pow(i, MOD - 2, MOD)
    h %= MOD
    ans = (2 * N % MOD) * (M * M % MOD) % MOD * h % MOD
    ans = (ans - M * M) % MOD
    print(ans)

main()
