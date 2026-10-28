import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    K = int(data[1])
    inv_n2 = pow(N * N % MOD, MOD - 2, MOD)
    # P = probability black ball at position 1
    # From position 1: moves away with prob 2(N-1)/N^2
    # From other position: moves to position 1 with prob 2/N^2
    stay = (1 - 2 * (N - 1) % MOD * inv_n2) % MOD
    come = 2 * inv_n2 % MOD
    P = 1
    for _ in range(K):
        P = (P * stay + (1 - P) * come) % MOD
    # E = P*1 + (1-P)*(N+2)/2
    inv2 = pow(2, MOD - 2, MOD)
    E = (P + (1 - P) % MOD * ((N + 2) % MOD) % MOD * inv2) % MOD
    print(E)

main()
