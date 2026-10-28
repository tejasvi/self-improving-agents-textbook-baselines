import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]

    FULL = (1 << 11) - 1  # bits 0..10 represent achievable subset sums
    TARGET = 1 << 10
    dp = [0] * (1 << 11)
    dp[1] = 1  # empty subset has sum 0

    for A in a:
        inv = pow(A, MOD - 2, MOD)
        ndp = [0] * (1 << 11)
        for mask in range(1 << 11):
            p = dp[mask]
            if p == 0:
                continue
            pi = p * inv % MOD
            # values v in 1..min(A,10)
            for v in range(1, min(A, 10) + 1):
                nm = (mask | (mask << v)) & FULL
                ndp[nm] = (ndp[nm] + pi) % MOD
            # values v > 10: mask unchanged
            if A > 10:
                cnt = A - 10
                ndp[mask] = (ndp[mask] + pi * cnt) % MOD
        dp = ndp

    ans = 0
    for mask in range(1 << 11):
        if mask & TARGET:
            ans = (ans + dp[mask]) % MOD
    print(ans)


main()
