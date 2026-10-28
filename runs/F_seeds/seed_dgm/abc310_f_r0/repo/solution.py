import sys

def main():
    MOD = 998244353
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    FULL = (1 << 11) - 1
    dp = [0] * (1 << 11)
    dp[1] = 1  # subset sum 0 achievable
    for a in A:
        inv = pow(a, MOD - 2, MOD)
        ndp = [0] * (1 << 11)
        for m in range(1 << 11):
            p = dp[m]
            if not p:
                continue
            pi = p * inv % MOD
            for v in range(1, min(a, 10) + 1):
                nm = (m | (m << v)) & FULL
                ndp[nm] = (ndp[nm] + pi) % MOD
            if a > 10:
                ndp[m] = (ndp[m] + pi * (a - 10)) % MOD
        dp = ndp
    ans = 0
    for m in range(1 << 11):
        if m >> 10 & 1:
            ans = (ans + dp[m]) % MOD
    print(ans)

main()
