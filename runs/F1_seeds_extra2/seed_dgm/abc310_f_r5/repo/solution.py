import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    FULL = (1 << 11) - 1
    dp = [0] * (1 << 11)
    dp[1] = 1  # sum 0 is reachable
    for A in a:
        invA = pow(A, MOD - 2, MOD)
        ndp = [0] * (1 << 11)
        big = max(0, A - 10)  # faces > 10 leave the mask unchanged
        lim = min(A, 10)
        for mask in range(1 << 11):
            cur = dp[mask]
            if cur == 0:
                continue
            w = cur * invA % MOD
            for v in range(1, lim + 1):
                nm = (mask | (mask << v)) & FULL
                ndp[nm] += w
            if big:
                ndp[mask] += w * big
        dp = [x % MOD for x in ndp]
    ans = 0
    for mask in range(1 << 11):
        if mask >> 10 & 1:
            ans += dp[mask]
    print(ans % MOD)


main()
