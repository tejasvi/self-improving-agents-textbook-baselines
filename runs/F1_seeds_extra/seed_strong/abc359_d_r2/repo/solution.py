import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0]); k = int(data[1]); s = data[2]
    MOD = 998244353
    m = k - 1
    full_size = 1 << k
    # palindrome table for k-bit masks (bit j = j-th char from the left)
    is_pal = [False] * full_size
    for x in range(full_size):
        bits = [(x >> (k - 1 - j)) & 1 for j in range(k)]
        is_pal[x] = bits == bits[::-1]
    mask_all = (1 << m) - 1
    dp = [0] * (1 << m)
    for mask in range(1 << m):
        ok = True
        for j in range(m):
            b = (mask >> (m - 1 - j)) & 1
            c = s[j]
            if (c == 'A' and b == 1) or (c == 'B' and b == 0):
                ok = False
                break
        if ok:
            dp[mask] = 1
    for i in range(m, n):
        c = s[i]
        choices = (0,) if c == 'A' else (1,) if c == 'B' else (0, 1)
        ndp = [0] * (1 << m)
        for mask in range(1 << m):
            v = dp[mask]
            if not v:
                continue
            for b in choices:
                full = (mask << 1) | b
                if is_pal[full]:
                    continue
                nm = full & mask_all
                ndp[nm] = (ndp[nm] + v) % MOD
        dp = ndp
    print(sum(dp) % MOD)

main()
