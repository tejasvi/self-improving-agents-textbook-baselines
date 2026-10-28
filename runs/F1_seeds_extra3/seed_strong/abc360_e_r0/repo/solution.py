import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    K = int(data[1])
    inv = lambda x: pow(x % MOD, MOD - 2, MOD)
    invN = inv(N)
    # a_k = P(black at position 1) after k steps
    r = (1 - 2 * invN) % MOD
    rk = pow(r, K, MOD)
    a = (invN + (1 - invN) % MOD * rk) % MOD
    half = inv(2)
    ans = (a + (1 - a) % MOD * ((N + 2) % MOD) % MOD * half) % MOD
    print(ans)

main()
