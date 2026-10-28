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
        inv = pow(a, MOD - 2, MOD)
        new = [0] * (1 << 11)
        lim = min(a, 10)
        stay = (a - 10) if a > 10 else 0
        for m in range(1 << 11):
            p = dp[m]
            if not p:
                continue
            p = p * inv % MOD
            for v in range(1, lim + 1):
                nm = (m | (m << v)) & FULL
                new[nm] = (new[nm] + p) % MOD
            if stay:
                new[m] = (new[m] + p * stay) % MOD
        dp = new
    ans = 0
    for m in range(1 << 11):
        if m >> 10 & 1:
            ans = (ans + dp[m]) % MOD
    print(ans)

main()
