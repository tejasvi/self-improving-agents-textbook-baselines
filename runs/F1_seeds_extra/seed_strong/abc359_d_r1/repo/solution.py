import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0]); k = int(data[1]); s = data[2]
    MOD = 998244353
    m = k - 1
    # palindrome table for k-bit windows
    pal = [False] * (1 << k)
    for w in range(1 << k):
        r = 0
        x = w
        for _ in range(k):
            r = (r << 1) | (x & 1)
            x >>= 1
        pal[w] = (r == w)
    # initial masks for first k-1 chars: char at position j -> bit (m-1-j)
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
    full = (1 << m) - 1
    for i in range(m, n):
        c = s[i]
        choices = []
        if c == 'A' or c == '?':
            choices.append(0)
        if c == 'B' or c == '?':
            choices.append(1)
        ndp = [0] * (1 << m)
        for mask in range(1 << m):
            v = dp[mask]
            if not v:
                continue
            for b in choices:
                w = (mask << 1) | b
                if pal[w]:
                    continue
                nm = w & full
                ndp[nm] = (ndp[nm] + v) % MOD
        dp = ndp
    print(sum(dp) % MOD)

main()
