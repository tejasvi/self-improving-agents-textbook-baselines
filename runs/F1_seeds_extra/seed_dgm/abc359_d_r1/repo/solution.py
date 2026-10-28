import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0]); k = int(data[1]); s = data[2]
    MOD = 998244353

    # palindrome table for K-bit windows
    pal = [False] * (1 << k)
    for m in range(1 << k):
        bits = [(m >> j) & 1 for j in range(k)]
        pal[m] = bits == bits[::-1]

    low_mask = (1 << (k - 1)) - 1
    dp = {0: 1}
    for i in range(n):
        ch = s[i]
        choices = []
        if ch == 'A':
            choices = [0]
        elif ch == 'B':
            choices = [1]
        else:
            choices = [0, 1]
        ndp = {}
        for mask, cnt in dp.items():
            for c in choices:
                full = (mask << 1) | c
                if i >= k - 1:
                    if pal[full & ((1 << k) - 1)]:
                        continue
                    nm = full & low_mask
                else:
                    nm = full
                ndp[nm] = (ndp.get(nm, 0) + cnt) % MOD
        dp = ndp
    print(sum(dp.values()) % MOD)

main()
