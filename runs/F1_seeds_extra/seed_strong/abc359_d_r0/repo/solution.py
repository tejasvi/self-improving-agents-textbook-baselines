import sys

def main():
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    s = data[2]
    MOD = 998244353
    L = k - 1
    size = 1 << L
    full_size = 1 << k
    # palindrome check for k-bit masks
    pal = [False] * full_size
    for f in range(full_size):
        ok = True
        for j in range(k // 2):
            if ((f >> j) & 1) != ((f >> (k - 1 - j)) & 1):
                ok = False
                break
        pal[f] = ok
    # allowed chars: 0 = A, 1 = B
    def allowed(ch):
        if ch == 'A':
            return (0,)
        if ch == 'B':
            return (1,)
        return (0, 1)
    dp = [0] * size
    for m in range(size):
        ok = True
        for j in range(L):
            bit = (m >> (L - 1 - j)) & 1
            if bit not in allowed(s[j]):
                ok = False
                break
        if ok:
            dp[m] = 1
    mask = size - 1
    for i in range(L, n):
        al = allowed(s[i])
        ndp = [0] * size
        for m in range(size):
            v = dp[m]
            if not v:
                continue
            for c in al:
                f = (m << 1) | c
                if pal[f]:
                    continue
                nm = f & mask
                ndp[nm] = (ndp[nm] + v) % MOD
        dp = ndp
    print(sum(dp) % MOD)

main()
