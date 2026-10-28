import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    FULL = (1 << 11) - 1
    dp = [0] * (1 << 11)
    dp[1] = 1  # sum 0 is always achievable
    total = 1
    for a in A:
        total = total * a % MOD
        new = [0] * (1 << 11)
        lim = min(a, 10)
        rest = max(0, a - 10)
        for m in range(1 << 11):
            c = dp[m]
            if c == 0:
                continue
            for v in range(1, lim + 1):
                nm = (m | (m << v)) & FULL
                new[nm] = (new[nm] + c) % MOD
            if rest:
                new[m] = (new[m] + c * rest) % MOD
        dp = new
    good = sum(dp[m] for m in range(1 << 11) if m >> 10 & 1) % MOD
    ans = good * pow(total, MOD - 2, MOD) % MOD
    print(ans)

main()
