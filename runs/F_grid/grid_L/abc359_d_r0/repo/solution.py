import sys

def main():
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    s = data[2]
    MOD = 998244353

    full = (1 << k) - 1
    is_pal = [False] * (1 << k)
    for w in range(1 << k):
        r = int(format(w, '0%db' % k)[::-1], 2)
        is_pal[w] = (r == w)

    low_mask = (1 << (k - 1)) - 1
    dp = [0] * (1 << (k - 1))
    dp[0] = 1
    # Track whether we've appended at least K-1 chars; before that, masks are
    # shorter and no palindrome check is applied.
    for i in range(n):
        ch = s[i]
        if ch == 'A':
            choices = (0,)
        elif ch == 'B':
            choices = (1,)
        else:
            choices = (0, 1)
        ndp = [0] * (1 << (k - 1))
        check = (i + 1 >= k)
        for m in range(1 << (k - 1)):
            v = dp[m]
            if not v:
                continue
            for c in choices:
                w = (m << 1) | c
                if check and is_pal[w & full]:
                    continue
                nm = w & low_mask
                ndp[nm] = (ndp[nm] + v) % MOD
        dp = ndp
    print(sum(dp) % MOD)

main()
