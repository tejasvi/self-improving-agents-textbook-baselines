import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    s = data[2]
    m = k - 1
    full = (1 << m) - 1

    def rev(x, bits):
        r = 0
        for _ in range(bits):
            r = (r << 1) | (x & 1)
            x >>= 1
        return r

    is_pal = [rev(w, k) == w for w in range(1 << k)]

    # Initial states: all masks of length m consistent with s[0:m].
    # Bit for position j (0-indexed) is at shift (m-1-j); 'B' = 1, 'A' = 0.
    dp = [0] * (1 << m)
    for mask in range(1 << m):
        ok = True
        for j in range(m):
            bit = (mask >> (m - 1 - j)) & 1
            c = s[j]
            if c == '?':
                continue
            if (c == 'B') != (bit == 1):
                ok = False
                break
        if ok:
            dp[mask] = 1

    for i in range(m, n):
        c = s[i]
        choices = (0, 1) if c == '?' else ((1,) if c == 'B' else (0,))
        ndp = [0] * (1 << m)
        for mask in range(1 << m):
            v = dp[mask]
            if not v:
                continue
            for b in choices:
                w = (mask << 1) | b
                if is_pal[w]:
                    continue
                nm = w & full
                ndp[nm] = (ndp[nm] + v) % MOD
        dp = ndp

    print(sum(dp) % MOD)

main()
