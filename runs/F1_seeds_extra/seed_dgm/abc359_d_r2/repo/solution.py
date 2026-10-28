import sys

def main():
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    s = data[2]
    MOD = 998244353
    m = k - 1
    full = 1 << m
    # palindrome table for K-bit windows
    is_pal = [False] * (1 << k)
    for w in range(1 << k):
        bits = [(w >> j) & 1 for j in range(k)]
        is_pal[w] = bits == bits[::-1]

    def allowed(c, bit):
        # bit: 0 for A, 1 for B
        if c == '?':
            return True
        return (c == 'B') == (bit == 1)

    # initial: masks of length m matching s[0:m]
    dp = [0] * full
    for mask in range(full):
        ok = True
        for j in range(m):
            b = (mask >> (m - 1 - j)) & 1
            if not allowed(s[j], b):
                ok = False
                break
        if ok:
            dp[mask] = 1

    lowmask = full - 1
    for i in range(m, n):
        c = s[i]
        ndp = [0] * full
        for mask in range(full):
            v = dp[mask]
            if not v:
                continue
            for b in (0, 1):
                if not allowed(c, b):
                    continue
                w = (mask << 1) | b
                if is_pal[w]:
                    continue
                nm = w & lowmask
                ndp[nm] = (ndp[nm] + v) % MOD
        dp = ndp

    print(sum(dp) % MOD)

main()
