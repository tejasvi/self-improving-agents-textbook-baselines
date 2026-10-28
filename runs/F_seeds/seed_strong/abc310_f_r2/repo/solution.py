import sys

def main():
    data = sys.stdin.read().split()
    MOD = 998244353
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    FULL = (1 << 11) - 1
    dp = [0] * (1 << 11)
    dp[1] = 1  # sum 0 reachable
    for a in A:
        ndp = [0] * (1 << 11)
        big = max(0, a - 10)
        lim = min(a, 10)
        for m in range(1 << 11):
            c = dp[m]
            if not c:
                continue
            for v in range(1, lim + 1):
                nm = (m | (m << v)) & FULL
                ndp[nm] += c
            if big:
                ndp[m] += c * big
        inv = pow(a, MOD - 2, MOD)
        dp = [x % MOD * inv % MOD for x in ndp]
    ans = 0
    for m in range(1 << 11):
        if m >> 10 & 1:
            ans += dp[m]
    print(ans % MOD)

main()
