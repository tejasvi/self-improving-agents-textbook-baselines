import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    s = data[2]

    L = k - 1
    full = 1 << L
    mask_low = full - 1

    # palindrome table for K-bit windows
    is_pal = [False] * (1 << k)
    for w in range(1 << k):
        bits = [(w >> (k - 1 - j)) & 1 for j in range(k)]
        is_pal[w] = bits == bits[::-1]

    def allowed(ch):
        if ch == 'A':
            return (0,)
        if ch == 'B':
            return (1,)
        return (0, 1)

    # initial states: all masks of length K-1 consistent with s[0..K-2]
    dp = [0] * full
    for m in range(full):
        ok = True
        for j in range(L):
            b = (m >> (L - 1 - j)) & 1
            if b not in allowed(s[j]):
                ok = False
                break
        if ok:
            dp[m] = 1

    for i in range(L, n):
        opts = allowed(s[i])
        ndp = [0] * full
        for m in range(full):
            v = dp[m]
            if not v:
                continue
            base = m << 1
            for c in opts:
                w = base | c
                if is_pal[w]:
                    continue
                nm = w & mask_low
                ndp[nm] = (ndp[nm] + v) % MOD
        dp = ndp

    print(sum(dp) % MOD)


main()
