import sys

MOD = 998244353


def main():
    N, K = map(int, sys.stdin.read().split())
    if N == 1:
        print(1)
        return
    inv_n2 = pow(N * N % MOD, MOD - 2, MOD)
    # P(black leaves position 1) = 2(N-1)/N^2 ; P(black moves 1 from another position) = 2/N^2
    leave = 2 * (N - 1) % MOD * inv_n2 % MOD
    enter = 2 * inv_n2 % MOD
    p = 1  # probability black ball is at position 1
    for _ in range(K):
        p = (p * (1 - leave) + (1 - p) * enter) % MOD
    # E[x] = p*1 + (1-p) * (average of positions 2..N) = p + (1-p)*(N+2)/2
    half = pow(2, MOD - 2, MOD)
    ans = (p + (1 - p) * ((N + 2) % MOD) % MOD * half) % MOD
    print(ans)


main()
