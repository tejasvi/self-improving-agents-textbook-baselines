import sys
from math import comb


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    s = data[2]
    MOD = 998244353
    bit = {'A': 1, 'B': 2, 'C': 4}
    # class index of a prefix xor value v: min(v, v^7) -> 4 classes
    cls = [0] * 8
    cid = {}
    for v in range(8):
        r = min(v, v ^ 7)
        if r not in cid:
            cid[r] = len(cid)
        cls[v] = cid[r]
    # state: (v, c0, c1, c2, c3) encoded as tuple -> count
    # prefix 0 (empty string): v=0
    cnt0 = [0, 0, 0, 0]
    cnt0[cls[0]] = 1
    dp = {(0, cnt0[0], cnt0[1], cnt0[2], cnt0[3]): 1}
    for i in range(n):
        ch = s[i]
        choices = [bit[ch]] if ch != '?' else [1, 2, 4]
        ndp = {}
        get = ndp.get
        for (v, a, b, c, d), w in dp.items():
            for bb in choices:
                nv = v ^ bb
                cc = cls[nv]
                if cc == 0:
                    key = (nv, a + 1, b, c, d)
                elif cc == 1:
                    key = (nv, a, b + 1, c, d)
                elif cc == 2:
                    key = (nv, a, b, c + 1, d)
                else:
                    key = (nv, a, b, c, d + 1)
                ndp[key] = (get(key, 0) + w) % MOD
        dp = ndp
    ans = 0
    for (v, a, b, c, d), w in dp.items():
        g = comb(a, 2) + comb(b, 2) + comb(c, 2) + comb(d, 2)
        if g >= k:
            ans += w
    print(ans % MOD)


main()
