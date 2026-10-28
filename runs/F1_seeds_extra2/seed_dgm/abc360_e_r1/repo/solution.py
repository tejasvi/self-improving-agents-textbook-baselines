import sys

MOD = 998244353

def main():
    N, K = map(int, sys.stdin.read().split())
    inv_n = pow(N, MOD - 2, MOD)
    # q_k = P(black ball at position 1) after K steps
    # q_k = 1/N + (1 - 1/N) * (1 - 2/N)^K
    c = (1 - 2 * inv_n) % MOD
    q = (inv_n + (1 - inv_n) % MOD * pow(c, K, MOD)) % MOD
    # E[x] = q * 1 + (1 - q) * (N + 2) / 2  (other positions 2..N are symmetric)
    avg = (N + 2) * pow(2, MOD - 2, MOD) % MOD
    ans = (q + (1 - q) % MOD * avg) % MOD
    print(ans)

main()
