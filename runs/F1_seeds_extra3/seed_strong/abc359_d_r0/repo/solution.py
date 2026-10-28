import sys

def main():
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    s = data[2]
    MOD = 998244353
    # pal[w] for K-bit window w
    pal = [False] * (1 << k)
    for w in range(1 << k):
        r = 0
        x = w
        for _ in range(k):
            r = (r << 1) | (x & 1)
            x >>= 1
        pal[w] = (r == w)
    lowmask = (1 << (k - 1)) - 1
    dp = [0] * (1 << (k - 1))
    dp[0] = 1
    # before any full window, states are prefixes of length i (value < 2^i)
    for i in range(n):
        ch = s[i]
        choices = (0, 1) if ch == '?' else ((0,) if ch == 'A' else (1,))
        size = 1 << (k - 1)
        ndp = [0] * size
        full = i + 1 >= k
        for m in range(size):
            v = dp[m]
            if v == 0:
                continue
            for c in choices:
                nm = (m << 1) | c
                if full:
                    if pal[nm]:
                        continue
                    nm &= lowmask
                ndp[nm] = (ndp[nm] + v) % MOD
        dp = ndp
    print(sum(dp) % MOD)

main()
