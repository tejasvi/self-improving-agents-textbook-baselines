import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    FULL = (1 << 11) - 1
    dp = {1: 1}  # bit 0: empty sum 0 always achievable
    for a in A:
        inv = pow(a, MOD - 2, MOD)
        ndp = {}
        big = max(0, a - 10)  # values > 10 leave mask unchanged
        for m, p in dp.items():
            pv = p * inv % MOD
            for v in range(1, min(a, 10) + 1):
                nm = (m | (m << v)) & FULL
                ndp[nm] = (ndp.get(nm, 0) + pv) % MOD
            if big:
                pb = pv * big % MOD
                ndp[m] = (ndp.get(m, 0) + pb) % MOD
        dp = ndp
    ans = 0
    for m, p in dp.items():
        if m >> 10 & 1:
            ans = (ans + p) % MOD
    print(ans)


main()
