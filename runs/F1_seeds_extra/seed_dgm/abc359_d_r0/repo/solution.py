import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    s = data[2]
    MOD = 998244353

    # pal[full]: whether the K-bit number (MSB = oldest char) is a palindrome
    pal = [False] * (1 << k)
    for full in range(1 << k):
        bits = [(full >> j) & 1 for j in range(k)]
        pal[full] = bits == bits[::-1]

    size = 1 << (k - 1)
    mask_keep = size - 1
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
        check = i >= k - 1
        for mask in range(size):
            v = dp[mask]
            if not v:
                continue
            for c in choices:
                full = (mask << 1) | c
                if check and pal[full]:
                    continue
                nm = full & mask_keep
                ndp[nm] = (ndp[nm] + v) % MOD
        dp = ndp
    print(sum(dp) % MOD)


main()
