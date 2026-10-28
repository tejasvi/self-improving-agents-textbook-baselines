import sys
from operator import mul

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    MOD = 998244353
    MAXV = max(A)
    phi = list(range(MAXV + 1))
    for p in range(2, MAXV + 1):
        if phi[p] == p:
            for k in range(p, MAXV + 1, p):
                phi[k] -= phi[k] // p
    needed = set(A)
    divlist = {v: [] for v in needed}
    for d in range(1, MAXV + 1):
        for k in range(d, MAXV + 1, d):
            if k in divlist:
                divlist[k].append(d)
    pre = {}
    for v in needed:
        ds = tuple(divlist[v])
        pre[v] = (ds, tuple(phi[d] for d in ds))
    C = [0] * (MAXV + 1)
    out = []
    R = 0
    w = 1
    for v in A:
        ds, ph = pre[v]
        # gcd(a, b) = sum_{d | gcd} phi(d)
        T = sum(map(mul, ph, map(C.__getitem__, ds))) % MOD
        R = (2 * R + T) % MOD
        out.append(R)
        for d in ds:
            C[d] += w
        w = w * 2 % MOD
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
