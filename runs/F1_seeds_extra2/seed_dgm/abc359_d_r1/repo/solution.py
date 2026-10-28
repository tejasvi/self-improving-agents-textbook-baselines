import sys

def main():
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    s = data[2]
    MOD = 998244353
    L = k - 1  # state: last L characters, first char is most significant bit
    # palindrome table for k-bit words
    pal = [False] * (1 << k)
    for w in range(1 << k):
        r = 0
        x = w
        for _ in range(k):
            r = (r << 1) | (x & 1)
            x >>= 1
        pal[w] = (r == w)

    def allowed(ch):
        if ch == 'A':
            return (0,)
        if ch == 'B':
            return (1,)
        return (0, 1)

    # initial: all masks of length L consistent with s[0:L]
    dp = [0] * (1 << L)
    for m in range(1 << L):
        ok = True
        for i in range(L):
            bit = (m >> (L - 1 - i)) & 1
            if bit not in allowed(s[i]):
                ok = False
                break
        if ok:
            dp[m] = 1
    full_mask = (1 << L) - 1
    for i in range(L, n):
        ch = allowed(s[i])
        ndp = [0] * (1 << L)
        for m in range(1 << L):
            v = dp[m]
            if not v:
                continue
            for c in ch:
                w = (m << 1) | c
                if pal[w]:
                    continue
                nm = w & full_mask
                ndp[nm] = (ndp[nm] + v) % MOD
        dp = ndp
    print(sum(dp) % MOD)

main()
