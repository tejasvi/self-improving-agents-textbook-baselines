import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    FULL = (1 << 11) - 1
    dp = [0] * (1 << 11)
    dp[1] = 1  # sum 0 is always reachable (empty subset)
    for a in A:
        inv = pow(a, MOD - 2, MOD)
        new = [0] * (1 << 11)
        lim = min(a, 10)
        for mask in range(1 << 11):
            cur = dp[mask]
            if not cur:
                continue
            for v in range(1, lim + 1):
                nm = (mask | (mask << v)) & FULL
                new[nm] = (new[nm] + cur) % MOD
            if a > 10:
                new[mask] = (new[mask] + cur * (a - 10)) % MOD
        dp = [x * inv % MOD for x in new]
    ans = 0
    for mask in range(1 << 11):
        if mask >> 10 & 1:
            ans = (ans + dp[mask]) % MOD
    print(ans)


main()
