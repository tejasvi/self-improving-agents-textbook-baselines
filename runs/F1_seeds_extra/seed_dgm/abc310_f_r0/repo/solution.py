import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    FULL = (1 << 11) - 1
    TARGET = 1 << 10
    dp = [0] * (1 << 11)
    dp[1] = 1  # empty subset gives sum 0
    for ai in a:
        inv = pow(ai, MOD - 2, MOD)
        ndp = [0] * (1 << 11)
        big = max(0, ai - 10)  # faces > 10 don't change the mask
        for mask in range(1 << 11):
            c = dp[mask]
            if not c:
                continue
            cw = c * inv % MOD
            for v in range(1, min(ai, 10) + 1):
                nm = (mask | (mask << v)) & FULL
                ndp[nm] = (ndp[nm] + cw) % MOD
            if big:
                ndp[mask] = (ndp[mask] + cw * big) % MOD
        dp = ndp
    ans = 0
    for mask in range(1 << 11):
        if mask & TARGET:
            ans = (ans + dp[mask]) % MOD
    print(ans)


main()
