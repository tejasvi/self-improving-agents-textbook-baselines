import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    FULL = (1 << 11) - 1
    dp = [0] * (1 << 11)
    dp[1] = 1  # empty subset achieves sum 0
    for a in A:
        inv = pow(a, MOD - 2, MOD)
        m = min(a, 10)
        keep = (a - m) % MOD
        ndp = [0] * (1 << 11)
        for mask in range(1 << 11):
            c = dp[mask]
            if not c:
                continue
            if keep:
                ndp[mask] = (ndp[mask] + c * keep) % MOD
            for v in range(1, m + 1):
                nm = (mask | (mask << v)) & FULL
                ndp[nm] = (ndp[nm] + c) % MOD
        dp = [x * inv % MOD for x in ndp]
    ans = 0
    for mask in range(1 << 11):
        if mask >> 10 & 1:
            ans = (ans + dp[mask]) % MOD
    print(ans)


main()
