import sys

MOD = 998244353

def main():
    N, K = map(int, sys.stdin.read().split())
    inv = lambda x: pow(x % MOD, MOD - 2, MOD)
    invN = inv(N)
    # q_t = P(black at position 1); q_{t+1} = q_t*(1-2/N) + 2/N^2
    r = (1 - 2 * invN) % MOD
    q = (1 - invN) * pow(r, K, MOD) % MOD
    q = (q + invN) % MOD
    # E = q + (1-q)*(N+2)/2
    half = inv(2)
    E = (q + (1 - q) * ((N + 2) % MOD) % MOD * half) % MOD
    print(E)

main()
