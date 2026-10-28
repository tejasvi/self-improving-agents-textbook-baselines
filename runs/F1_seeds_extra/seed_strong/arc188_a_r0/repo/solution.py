import sys
from math import comb

def main():
    data = sys.stdin.read().split()
    n = int(data[0]); k = int(data[1]); s = data[2]
    MOD = 998244353
    # state: (mask, n0, n1, n2, n3) where n_c = number of prefixes in class c
    # prefix mask bits: A->1, B->2, C->4; class of mask m is min(m, 7-m)
    dp = {(0, 1, 0, 0, 0): 1}
    for ch in s:
        if ch == 'A':
            flips = (1,)
        elif ch == 'B':
            flips = (2,)
        elif ch == 'C':
            flips = (4,)
        else:
            flips = (1, 2, 4)
        ndp = {}
        for (m, a, b, c, d), w in dp.items():
            for f in flips:
                nm = m ^ f
                cls = nm if nm < 4 else 7 - nm
                key = list((nm, a, b, c, d))
                key[1 + cls] += 1
                t = tuple(key)
                v = ndp.get(t, 0) + w
                ndp[t] = v % MOD if v >= MOD else v
        dp = ndp
    total = 0
    for (m, a, b, c, d), w in dp.items():
        good = comb(a, 2) + comb(b, 2) + comb(c, 2) + comb(d, 2)
        if good >= k:
            total += w
    print(total % MOD)

main()
