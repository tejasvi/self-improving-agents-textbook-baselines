import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    s = data[2]
    MOD = 998244353

    # palindrome check for k-bit windows
    def is_pal(x):
        bits = [(x >> j) & 1 for j in range(k)]
        return bits == bits[::-1]

    pal = [is_pal(x) for x in range(1 << k)]

    m = k - 1
    full_mask = (1 << m) - 1

    def allowed(ch):
        if ch == 'A':
            return (0,)
        if ch == 'B':
            return (1,)
        return (0, 1)

    # initial states: first k-1 characters
    dp = [0] * (1 << m)
    for mask in range(1 << m):
        ok = True
        for p in range(m):
            bit = (mask >> (m - 1 - p)) & 1
            if bit not in allowed(s[p]):
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
            base = mask << 1
            for c in opts:
                w = base | c
                if pal[w]:
                    continue
                nm = w & full_mask
                ndp[nm] = (ndp[nm] + v) % MOD
        dp = ndp

    print(sum(dp) % MOD)


main()
