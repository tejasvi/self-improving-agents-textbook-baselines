import sys

def main():
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    s = data[2]
    MOD = 998244353
    size = 1 << (k - 1)
    # pal[m]: whether the k-bit string m is a palindrome
    pal = [False] * (1 << k)
    for m in range(1 << k):
        r = 0
        x = m
        for _ in range(k):
            r = (r << 1) | (x & 1)
            x >>= 1
        pal[m] = (r == m)
    mask_low = size - 1
    dp = [0] * size
    dp[0] = 1
    for i, ch in enumerate(s):
        if ch == 'A':
            choices = (0,)
        elif ch == 'B':
            choices = (1,)
        else:
            choices = (0, 1)
        ndp = [0] * size
        full = i >= k - 1
        for m in range(size):
            v = dp[m]
            if not v:
                continue
            for c in choices:
                nm = (m << 1) | c
                if full:
                    if pal[nm]:
                        continue
                    nm &= mask_low
                ndp[nm] = (ndp[nm] + v) % MOD
        dp = ndp
    print(sum(dp) % MOD)

main()
