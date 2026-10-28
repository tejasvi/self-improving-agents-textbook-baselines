import sys

def main():
    MOD = 998244353
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    FULL = (1 << 11) - 1
    dp = [0] * (1 << 11)
    dp[1] = 1  # only subset sum 0 achievable
    for a in A:
        inv = pow(a, MOD - 2, MOD)
        ndp = [0] * (1 << 11)
        small = min(a, 10)
        big = max(0, a - 10)
        for mask in range(1 << 11):
            c = dp[mask]
            if not c:
                continue
            for v in range(1, small + 1):
                nm = (mask | (mask << v)) & FULL
                ndp[nm] += c
            if big:
                ndp[mask] += c * big
        dp = [x % MOD * inv % MOD for x in ndp]
    ans = 0
    for mask in range(1 << 11):
        if mask >> 10 & 1:
            ans += dp[mask]
    print(ans % MOD)

main()
