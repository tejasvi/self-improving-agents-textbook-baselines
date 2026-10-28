import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0]); k = int(data[1]); s = data[2]
    MOD = 998244353
    m = k - 1
    full = 1 << k
    # pal[w]: K-bit window w is a palindrome
    pal = [False] * full
    for w in range(full):
        r = 0
        x = w
        for _ in range(k):
            r = (r << 1) | (x & 1)
            x >>= 1
        pal[w] = (r == w)
    smask = (1 << m) - 1
    # dp over the last m characters (bit order: oldest is highest bit)
    dp = [0] * (1 << m)
    for mask in range(1 << m):
        ok = True
        for j in range(m):
            b = (mask >> (m - 1 - j)) & 1
            c = s[j]
            if c == '?':
                continue
            if (c == 'B') != (b == 1):
                ok = False
                break
        if ok:
            dp[mask] = 1
    for i in range(m, n):
        c = s[i]
        choices = (0, 1) if c == '?' else ((1,) if c == 'B' else (0,))
        ndp = [0] * (1 << m)
        for st in range(1 << m):
            v = dp[st]
            if not v:
                continue
            for b in choices:
                w = (st << 1) | b
                if pal[w]:
                    continue
                ns = w & smask
                ndp[ns] = (ndp[ns] + v) % MOD
        dp = ndp
    print(sum(dp) % MOD)

main()
