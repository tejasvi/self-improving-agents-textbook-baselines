import sys

def main():
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    s = data[2]
    MOD = 998244353

    # pal[x] for K-bit masks x: True if the K-bit string is a palindrome
    pal = [False] * (1 << k)
    for x in range(1 << k):
        bits = [(x >> j) & 1 for j in range(k)]
        pal[x] = bits == bits[::-1]

    m = k - 1
    full_mask = (1 << m) - 1
    size = 1 << m
    dp = [0] * size
    dp[0] = 1
    for i in range(n):
        ch = s[i]
        choices = []
        if ch == 'A':
            choices = [0]
        elif ch == 'B':
            choices = [1]
        else:
            choices = [0, 1]
        L = min(i, m)  # number of valid bits in state
        ndp = [0] * size
        for mask in range(size):
            v = dp[mask]
            if v == 0:
                continue
            for c in choices:
                w = (mask << 1) | c
                if L + 1 == k:
                    if pal[w]:
                        continue
                    nm = w & full_mask
                else:
                    nm = w
                ndp[nm] = (ndp[nm] + v) % MOD
        dp = ndp
    print(sum(dp) % MOD)

main()
