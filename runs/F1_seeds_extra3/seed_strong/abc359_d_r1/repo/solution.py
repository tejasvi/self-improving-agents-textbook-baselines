import sys

def main():
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    s = data[2]
    MOD = 998244353
    # palindrome table for k-bit windows
    pal = [False] * (1 << k)
    for w in range(1 << k):
        bits = [(w >> j) & 1 for j in range(k)]
        pal[w] = bits == bits[::-1]
    full_mask = (1 << k) - 1
    keep_mask = (1 << (k - 1)) - 1
    dp = {0: 1}
    for i in range(n):
        ch = s[i]
        opts = (0, 1) if ch == '?' else ((0,) if ch == 'A' else (1,))
        ndp = {}
        for mask, cnt in dp.items():
            for c in opts:
                full = (mask << 1) | c
                if i + 1 >= k:
                    if pal[full & full_mask]:
                        continue
                    nm = full & keep_mask
                else:
                    nm = full
                ndp[nm] = (ndp.get(nm, 0) + cnt) % MOD
        dp = ndp
    print(sum(dp.values()) % MOD)

main()
