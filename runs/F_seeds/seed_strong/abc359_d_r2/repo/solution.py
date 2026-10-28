import sys

def main():
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    s = data[2]
    MOD = 998244353
    m = k - 1
    full = 1 << m
    # palindrome table for K-bit windows
    def rev(w, bits):
        r = 0
        for _ in range(bits):
            r = (r << 1) | (w & 1)
            w >>= 1
        return r
    pal = [rev(w, k) == w for w in range(1 << k)]
    # initial states: first m characters
    dp = [0] * full
    for mask in range(full):
        ok = True
        for j in range(m):
            bit = (mask >> (m - 1 - j)) & 1  # 1 = 'B', 0 = 'A'
            ch = s[j]
            if ch == 'A' and bit == 1 or ch == 'B' and bit == 0:
                ok = False
                break
        if ok:
            dp[mask] = 1
    for i in range(m, n):
        ch = s[i]
        choices = []
        if ch != 'B':
            choices.append(0)
        if ch != 'A':
            choices.append(1)
        ndp = [0] * full
        for st in range(full):
            v = dp[st]
            if not v:
                continue
            for c in choices:
                w = (st << 1) | c
                if pal[w]:
                    continue
                ns = w & (full - 1)
                ndp[ns] = (ndp[ns] + v) % MOD
        dp = ndp
    print(sum(dp) % MOD)

main()
