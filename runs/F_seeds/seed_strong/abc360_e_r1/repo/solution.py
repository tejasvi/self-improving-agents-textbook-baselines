import sys

MOD = 998244353

def main():
    N, K = map(int, sys.stdin.read().split())
    inv_n = pow(N, MOD - 2, MOD)
    # P(black at position 1) after K steps: p_k = 1/N + (N-1)/N * (1-2/N)^k
    r = (1 - 2 * inv_n) % MOD
    p = (inv_n + (N - 1) * inv_n % MOD * pow(r, K, MOD)) % MOD
    # E[x] = p*1 + (1-p) * (N+2)/2
    half_avg = (N + 2) * pow(2, MOD - 2, MOD) % MOD
    ans = (p + (1 - p) % MOD * half_avg) % MOD
    print(ans)

main()
