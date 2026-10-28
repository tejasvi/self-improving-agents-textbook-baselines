import sys

def main():
    MOD = 998244353
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    FULL = (1 << 11) - 1
    dp = [0] * (1 << 11)
    dp[1] = 1  # sum 0 achievable
    for a in A:
        inv = pow(a, MOD - 2, MOD)
        ndp = [0] * (1 << 11)
        big = max(0, a - 10)  # values > 10 leave mask unchanged
        for mask in range(1 << 11):
            cur = dp[mask]
            if cur == 0:
                continue
            w = cur * inv % MOD
            for v in range(1, min(a, 10) + 1):
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
