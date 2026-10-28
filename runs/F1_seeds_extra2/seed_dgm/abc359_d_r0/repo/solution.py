import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0]); k = int(data[1]); s = data[2]
    MOD = 998244353

    # palindrome table for K-bit windows
    pal = [False] * (1 << k)
    for w in range(1 << k):
        bits = [(w >> j) & 1 for j in range(k)]
        pal[w] = bits == bits[::-1]

    m = k - 1
    size = 1 << m
    low_mask = size - 1
    full_mask = (1 << k) - 1

    dp = [0] * size
    dp[0] = 1
    for i in range(n):
        ch = s[i]
        if ch == 'A':
            choices = (0,)
        elif ch == 'B':
            choices = (1,)
        else:
            choices = (0, 1)
        ndp = [0] * size
        for mask in range(size):
            v = dp[mask]
            if v == 0:
                continue
            for c in choices:
                nf = (mask << 1) | c
                if i + 1 >= k and pal[nf & full_mask]:
                    continue
                nm = nf & low_mask
                ndp[nm] = (ndp[nm] + v) % MOD
        dp = ndp

    print(sum(dp) % MOD)

main()
