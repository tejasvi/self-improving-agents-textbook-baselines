import sys

def main():
    data = sys.stdin.read().split()
    MOD = 998244353
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    FULL = (1 << 11) - 1
    dp = [0] * (1 << 11)
    dp[1] = 1  # bit 0: empty subset sum 0
    for a in A:
        inv = pow(a, MOD - 2, MOD)
        new = [0] * (1 << 11)
        lim = min(a, 10)
        stay = max(0, a - 10)
        for m in range(1 << 11):
            c = dp[m]
            if not c:
                continue
            if stay:
                new[m] = (new[m] + c * stay) % MOD
            for v in range(1, lim + 1):
                nm = (m | (m << v)) & FULL
                new[nm] = (new[nm] + c) % MOD
        dp = [x * inv % MOD for x in new]
    ans = sum(dp[m] for m in range(1 << 11) if m >> 10 & 1) % MOD
    print(ans)

main()
