import sys

def main():
    MOD = 998244353
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    FULL = (1 << 11) - 1  # bits 0..10 represent achievable subset sums
    dp = {1: 1}  # only sum 0 achievable
    for a in A:
        inv = pow(a, MOD - 2, MOD)
        ndp = {}
        lim = min(a, 10)
        rest = (a - 10) * inv % MOD if a > 10 else 0
        for mask, p in dp.items():
            pi = p * inv % MOD
            for v in range(1, lim + 1):
                nm = (mask | (mask << v)) & FULL
                ndp[nm] = (ndp.get(nm, 0) + pi) % MOD
            if rest:
                ndp[mask] = (ndp.get(mask, 0) + p * rest) % MOD
        dp = ndp
    ans = 0
    for mask, p in dp.items():
        if mask >> 10 & 1:
            ans = (ans + p) % MOD
    print(ans)

main()
