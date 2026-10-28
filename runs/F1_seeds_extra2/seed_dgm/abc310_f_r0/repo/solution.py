import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    FULL = (1 << 11) - 1
    dp = [0] * (1 << 11)
    dp[1] = 1  # sum 0 is always achievable
    for ai in a:
        inv = pow(ai, MOD - 2, MOD)
        ndp = [0] * (1 << 11)
        for m in range(1 << 11):
            cur = dp[m]
            if not cur:
                continue
            w = cur * inv % MOD
            for v in range(1, min(ai, 10) + 1):
                nm = (m | (m << v)) & FULL
                ndp[nm] = (ndp[nm] + w) % MOD
            if ai > 10:
                ndp[m] = (ndp[m] + w * (ai - 10)) % MOD
        dp = ndp
    ans = 0
    for m in range(1 << 11):
        if m >> 10 & 1:
            ans = (ans + dp[m]) % MOD
    print(ans)


main()
