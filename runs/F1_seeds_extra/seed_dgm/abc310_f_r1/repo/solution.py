import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    FULL = (1 << 11) - 1
    dp = [0] * (1 << 11)
    dp[1] = 1  # sum 0 is always achievable
    for A in a:
        inv = pow(A, MOD - 2, MOD)
        small = min(A, 10)
        big = A - small
        new = [0] * (1 << 11)
        for m in range(1 << 11):
            w = dp[m]
            if not w:
                continue
            w = w * inv % MOD
            for v in range(1, small + 1):
                nm = (m | (m << v)) & FULL
                new[nm] = (new[nm] + w) % MOD
            if big:
                new[m] = (new[m] + w * big) % MOD
        dp = new
    ans = 0
    for m in range(1 << 11):
        if m >> 10 & 1:
            ans = (ans + dp[m]) % MOD
    print(ans)


main()
