import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    inv_n2 = pow(n * n % MOD, MOD - 2, MOD)
    stay = (1 - 2 * (n - 1) % MOD * inv_n2) % MOD   # P(stay at 1 | at 1)
    come = 2 * inv_n2 % MOD                          # P(move to 1 | not at 1)
    p = 1  # probability black ball is at position 1
    for _ in range(k):
        p = (p * stay + (1 - p) * come) % MOD
    half = (n + 2) * pow(2, MOD - 2, MOD) % MOD
    ans = (p + (1 - p) * half) % MOD
    print(ans)


main()
