import sys

def main():
    MOD = 998244353
    N, M = map(int, sys.stdin.read().split())
    # answer = M^2 * (2N * H_N - 1)  mod p
    inv = [0, 1] + [0] * (N - 1)
    for i in range(2, N + 1):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD
    H = 0
    for i in range(1, N + 1):
        H += inv[i]
    H %= MOD
    ans = (M * M % MOD) * ((2 * N % MOD) * H % MOD - 1) % MOD
    print(ans % MOD)

main()
