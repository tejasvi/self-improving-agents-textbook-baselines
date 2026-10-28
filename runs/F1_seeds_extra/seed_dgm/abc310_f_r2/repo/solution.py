import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    FULL = (1 << 11) - 1
    dp = [0] * (1 << 11)
    dp[1] = 1  # subset sum 0 reachable
    for ai in a:
        inv = pow(ai, MOD - 2, MOD)
        ndp = [0] * (1 << 11)
        for mask in range(1 << 11):
            p = dp[mask]
            if p == 0:
                continue
            p_inv = p * inv % MOD
            # faces v > 10 leave the mask unchanged
            cnt_big = max(0, ai - 10)
            if cnt_big:
                ndp[mask] = (ndp[mask] + p_inv * cnt_big) % MOD
            for v in range(1, min(ai, 10) + 1):
                nm = (mask | (mask << v)) & FULL
                ndp[nm] = (ndp[nm] + p_inv) % MOD
        dp = ndp
    ans = 0
    for mask in range(1 << 11):
        if mask >> 10 & 1:
            ans = (ans + dp[mask]) % MOD
    print(ans)


main()
