import sys

def main():
    data = sys.stdin.read().split()
    MOD = 998244353
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    FULL = (1 << 11) - 1
    dp = [0] * (1 << 11)
    dp[1] = 1  # sum 0 always achievable
    for a in A:
        inv = pow(a, MOD - 2, MOD)
        ndp = [0] * (1 << 11)
        lim = min(a, 10)
        big = (a - 10) * inv % MOD if a > 10 else 0
        for mask in range(1 << 11):
            p = dp[mask]
            if not p:
                continue
            q = p * inv % MOD
            for v in range(1, lim + 1):
                nm = (mask | (mask << v)) & FULL
                ndp[nm] = (ndp[nm] + q) % MOD
            if big:
                ndp[mask] = (ndp[mask] + p * big) % MOD
        dp = ndp
    ans = 0
    for mask in range(1 << 11):
        if mask >> 10 & 1:
            ans = (ans + dp[mask]) % MOD
    print(ans)

main()
