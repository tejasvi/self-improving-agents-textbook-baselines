import sys

MOD = 998244353

def main():
    N, K = map(int, sys.stdin.read().split())
    if N == 1:
        print(1)
        return
    inv = lambda x: pow(x % MOD, MOD - 2, MOD)
    inv_n2 = inv(N * N % MOD)
    b = 2 * inv_n2 % MOD                       # prob to move to a specific other position
    a = (1 - 2 * (N - 1) % MOD * inv_n2) % MOD  # prob to stay
    # p = prob black ball at position 1
    p = 1
    for _ in range(K):
        p = (p * a + (1 - p) * b) % MOD
    # E = p + (1-p)*(N+2)/2
    half = (N + 2) * inv(2) % MOD
    ans = (p + (1 - p) * half) % MOD
    print(ans)

main()
