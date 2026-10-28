import sys

def main():
    MOD = 998244353
    N, K = map(int, sys.stdin.read().split())
    inv_n2 = pow(N * N % MOD, MOD - 2, MOD)
    t = 2 * inv_n2 % MOD                      # prob to move to a specific other position
    s = (1 - 2 * (N - 1) % MOD * inv_n2) % MOD  # prob to stay
    a = 1  # prob black ball at its original position
    for _ in range(K):
        a = (a * s + (1 - a) * t) % MOD
    half = pow(2, MOD - 2, MOD)
    ans = (a + (1 - a) * ((N + 2) % MOD) % MOD * half) % MOD
    print(ans)

main()
