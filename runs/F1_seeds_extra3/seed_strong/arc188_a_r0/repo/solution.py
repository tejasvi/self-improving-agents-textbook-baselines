import sys
from math import comb

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    K = int(data[1])
    S = data[2]
    # class of parity vector v: {v, v^7} -> id min(v, v^7) in 0..3
    cls = [min(v, v ^ 7) for v in range(8)]
    # DP state: (v, n0, n1, n2, n3) -> count
    # encode n-vector as tuple
    init_n = [0, 0, 0, 0]
    init_n[cls[0]] = 1
    dp = {(0, tuple(init_n)): 1}
    for i in range(N):
        ch = S[i]
        if ch == 'A':
            opts = [0]
        elif ch == 'B':
            opts = [1]
        elif ch == 'C':
            opts = [2]
        else:
            opts = [0, 1, 2]
        ndp = {}
        get = ndp.get
        for (v, n), c in dp.items():
            for x in opts:
                nv = v ^ (1 << x)
                k = cls[nv]
                nl = list(n)
                nl[k] += 1
                key = (nv, tuple(nl))
                ndp[key] = (get(key, 0) + c) % MOD
        dp = ndp
    ans = 0
    for (v, n), c in dp.items():
        g = sum(comb(x, 2) for x in n)
        if g >= K:
            ans = (ans + c) % MOD
    print(ans % MOD)


main()
