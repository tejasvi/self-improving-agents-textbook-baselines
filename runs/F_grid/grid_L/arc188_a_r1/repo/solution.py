import sys
from math import comb

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    s = data[2]
    # Prefix parity vector v (3 bits: A,B,C). Substring (i,j] good iff
    # P_i ^ P_j in {000,111}, i.e. same class where class(v)=min(v, v^7).
    # Total good substrings = sum over classes C(m_c, 2), m_c = #prefixes in class c.
    bit = {'A': 1, 'B': 2, 'C': 4}
    # state: (P, m0, m1, m2, m3) -> count
    dp = {(0, 1, 0, 0, 0): 1}
    for ch in s:
        if ch == '?':
            opts = [1, 2, 4]
        else:
            opts = [bit[ch]]
        ndp = {}
        for (p, m0, m1, m2, m3), cnt in dp.items():
            for o in opts:
                q = p ^ o
                c = min(q, q ^ 7)
                if c == 0:
                    key = (q, m0 + 1, m1, m2, m3)
                elif c == 1:
                    key = (q, m0, m1 + 1, m2, m3)
                elif c == 2:
                    key = (q, m0, m1, m2 + 1, m3)
                else:
                    key = (q, m0, m1, m2, m3 + 1)
                ndp[key] = (ndp.get(key, 0) + cnt) % MOD
        dp = ndp
    ans = 0
    for (p, m0, m1, m2, m3), cnt in dp.items():
        g = comb(m0, 2) + comb(m1, 2) + comb(m2, 2) + comb(m3, 2)
        if g >= k:
            ans = (ans + cnt) % MOD
    print(ans)


main()
