import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]

    FULL = (1 << 11) - 1
    dp = [0] * (1 << 11)
    dp[1] = 1  # sum 0 is always reachable (empty selection)
    prod = 1
    for A in a:
        prod = prod * A % MOD
        ndp = [0] * (1 << 11)
        big = max(0, A - 10)  # values > 10 don't change the reachable set
        small = min(A, 10)
        for mask in range(1 << 11):
            c = dp[mask]
            if c == 0:
                continue
            if big:
                ndp[mask] = (ndp[mask] + c * big) % MOD
            for v in range(1, small + 1):
                nm = (mask | (mask << v)) & FULL
                ndp[nm] = (ndp[nm] + c) % MOD
        dp = ndp

    total = 0
    for mask in range(1 << 11):
        if mask >> 10 & 1:
            total += dp[mask]
    total %= MOD
    ans = total * pow(prod, MOD - 2, MOD) % MOD
    print(ans)


main()
