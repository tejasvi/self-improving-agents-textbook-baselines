import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    s = data[2]
    MOD = 998244353

    def is_pal(w):
        # w is a k-bit number; check if its k-bit representation is a palindrome
        for i in range(k // 2):
            if ((w >> i) & 1) != ((w >> (k - 1 - i)) & 1):
                return False
        return True

    pal = [is_pal(w) for w in range(1 << k)]
    low_mask = (1 << (k - 1)) - 1

    dp = {0: 1}
    for i, ch in enumerate(s):
        if ch == 'A':
            opts = (0,)
        elif ch == 'B':
            opts = (1,)
        else:
            opts = (0, 1)
        ndp = {}
        for mask, cnt in dp.items():
            for c in opts:
                nw = (mask << 1) | c
                if i + 1 >= k:
                    if pal[nw]:
                        continue
                    nm = nw & low_mask
                else:
                    nm = nw
                ndp[nm] = (ndp.get(nm, 0) + cnt) % MOD
        dp = ndp

    print(sum(dp.values()) % MOD)

main()
