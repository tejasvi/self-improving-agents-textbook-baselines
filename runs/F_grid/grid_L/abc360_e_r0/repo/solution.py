import sys

MOD = 998244353

def main():
    N, K = map(int, sys.stdin.read().split())
    if N == 1:
        print(1)
        return
    inv_n2 = pow(N * N % MOD, MOD - 2, MOD)
    stay = (1 - 2 * (N - 1) % MOD * inv_n2) % MOD   # black at 1 stays at 1
    come = 2 * inv_n2 % MOD                          # black elsewhere moves to 1
    p = 1
    for _ in range(K):
        p = (p * stay + (1 - p) * come) % MOD
    half_n2 = (N + 2) * pow(2, MOD - 2, MOD) % MOD
    ans = (p + (1 - p) * half_n2) % MOD
    print(ans)

main()
