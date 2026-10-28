import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    s = data[2]

    # pal[x]: whether the k-bit number x reads the same reversed
    pal = [False] * (1 << k)
    for x in range(1 << k):
        ok = True
        for j in range(k // 2):
            if ((x >> j) & 1) != ((x >> (k - 1 - j)) & 1):
                ok = False
                break
        pal[x] = ok

    m = k - 1
    full_mask = (1 << m) - 1

    # Initial states: all m-bit masks consistent with s[0:m].
    # The first character is the most significant bit.
    dp = [0] * (1 << m)
    for mask in range(1 << m):
        ok = True
        for j in range(m):
            bit = (mask >> (m - 1 - j)) & 1
            c = s[j]
            if c == 'A' and bit != 0:
                ok = False
                break
            if c == 'B' and bit != 1:
                ok = False
                break
        if ok:
            dp[mask] = 1

    for i in range(m, n):
        c = s[i]
        choices = []
        if c != 'B':
            choices.append(0)  # 'A' = 0
        if c != 'A':
            choices.append(1)  # 'B' = 1
        ndp = [0] * (1 << m)
        for mask in range(1 << m):
            v = dp[mask]
            if v == 0:
                continue
            base = mask << 1
            for b in choices:
                full = base | b
                if pal[full]:
                    continue
                nm = full & full_mask
                ndp[nm] = (ndp[nm] + v) % MOD
        dp = ndp

    print(sum(dp) % MOD)


main()
