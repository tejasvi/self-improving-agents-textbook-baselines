import sys
from math import comb

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); K = int(data[1]); S = data[2]
    MOD = 998244353
    # class of a parity mask m: min(m, m^7), relabeled to 0..3
    cls_id = {}
    cls_of = [0] * 8
    for m in range(8):
        r = min(m, m ^ 7)
        if r not in cls_id:
            cls_id[r] = len(cls_id)
        cls_of[m] = cls_id[r]
    # initial: prefix 0 with mask 0
    n0 = [0, 0, 0, 0]
    n0[cls_of[0]] = 1
    dp = {(0, tuple(n0)): 1}
    for ch in S:
        if ch == 'A':
            opts = [1]
        elif ch == 'B':
            opts = [2]
        elif ch == 'C':
            opts = [4]
        else:
            opts = [1, 2, 4]
        ndp = {}
        for (m, n), v in dp.items():
            for d in opts:
                m2 = m ^ d
                c = cls_of[m2]
                nl = list(n)
                nl[c] += 1
                key = (m2, tuple(nl))
                ndp[key] = (ndp.get(key, 0) + v) % MOD
        dp = ndp
    ans = 0
    for (m, n), v in dp.items():
        g = sum(comb(x, 2) for x in n)
        if g >= K:
            ans = (ans + v) % MOD
    print(ans)

main()
