import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    FULL = (1 << 11) - 1
    dp = [0] * (1 << 11)
    dp[1] = 1  # sum 0 is always achievable
    total = 1
    for A in a:
        total = total * A % MOD
        ndp = [0] * (1 << 11)
        small = min(A, 10)
        stay = max(0, A - 10)
        for mask in range(1 << 11):
            c = dp[mask]
            if not c:
                continue
            for v in range(1, small + 1):
                nm = (mask | (mask << v)) & FULL
                ndp[nm] = (ndp[nm] + c) % MOD
            if stay:
                ndp[mask] = (ndp[mask] + c * stay) % MOD
        dp = ndp
    good = 0
    for mask in range(1 << 11):
        if mask >> 10 & 1:
            good = (good + dp[mask]) % MOD
    ans = good * pow(total, MOD - 2, MOD) % MOD
    print(ans)


main()
