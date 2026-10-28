import sys

def main():
    MOD = 998244353
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    FULL = (1 << 11) - 1
    # mask bit s set <=> sum s is achievable using chosen dice (sums capped at 10)
    dp = [0] * (1 << 11)
    dp[1] = 1  # empty subset gives sum 0
    for a in A:
        inv = pow(a, MOD - 2, MOD)
        ndp = [0] * (1 << 11)
        big = max(0, a - 10) % MOD * inv % MOD  # values > 10 leave mask unchanged
        lim = min(a, 10)
        for m in range(1 << 11):
            p = dp[m]
            if p == 0:
                continue
            if big:
                ndp[m] = (ndp[m] + p * big) % MOD
            for v in range(1, lim + 1):
                nm = (m | (m << v)) & FULL
                ndp[nm] = (ndp[nm] + p * inv) % MOD
        dp = ndp
    ans = 0
    for m in range(1 << 11):
        if m >> 10 & 1:
            ans = (ans + dp[m]) % MOD
    print(ans)

main()
