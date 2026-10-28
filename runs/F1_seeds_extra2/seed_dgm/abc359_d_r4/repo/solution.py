import sys

def main():
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    s = data[2]
    MOD = 998244353
    m = k - 1
    full = 1 << k
    # pal[w]: K-bit window w (MSB = first char) is a palindrome
    pal = [False] * full
    for w in range(full):
        bits = [(w >> (k - 1 - j)) & 1 for j in range(k)]
        pal[w] = bits == bits[::-1]
    mask_m = (1 << m) - 1

    def allowed(ch):
        if ch == 'A':
            return (0,)
        if ch == 'B':
            return (1,)
        return (0, 1)

    # initial: all prefixes of length m matching S
    dp = [0] * (1 << m)
    for mask in range(1 << m):
        ok = True
        for j in range(m):
            b = (mask >> (m - 1 - j)) & 1
            if b not in allowed(s[j]):
                ok = False
                break
        if ok:
            dp[mask] = 1

    for i in range(m, n):
        opts = allowed(s[i])
        ndp = [0] * (1 << m)
        for mask in range(1 << m):
            v = dp[mask]
            if not v:
                continue
            for c in opts:
                w = (mask << 1) | c
                if pal[w]:
                    continue
                nm = w & mask_m
                ndp[nm] = (ndp[nm] + v) % MOD
        dp = ndp

    print(sum(dp) % MOD)

main()
