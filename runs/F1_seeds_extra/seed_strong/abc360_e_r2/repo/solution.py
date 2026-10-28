import sys

MOD = 998244353

def main():
    N, K = map(int, sys.stdin.read().split())
    inv_n2 = pow(N * N % MOD, MOD - 2, MOD)
    # P(black ball at a specific position moves away / to a specific other position)
    move_out = 2 * (N - 1) % MOD * inv_n2 % MOD
    s = (1 - move_out) % MOD
    t = 2 * inv_n2 % MOD  # prob to move to position 1 from a specific other position
    a = 1  # probability black ball is at position 1
    for _ in range(K):
        a = (a * s + (1 - a) * t) % MOD
    # E = a*1 + (1-a) * (N+2)/2  (other positions are uniformly likely)
    inv2 = (MOD + 1) // 2
    ans = (a + (1 - a) % MOD * ((N + 2) % MOD) % MOD * inv2) % MOD
    print(ans)

main()
