import sys
from operator import mul
def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    MOD = 998244353
    M = max(A)
    phi = list(range(M + 1))
    for p in range(2, M + 1):
        if phi[p] == p:
            for q in range(p, M + 1, p):
                phi[q] -= phi[q] // p
    present = [False] * (M + 1)
    for a in A:
        present[a] = True
    divs = [None] * (M + 1)
    for d in range(1, M + 1):
        for m in range(d, M + 1, d):
            if present[m]:
                if divs[m] is None:
                    divs[m] = []
                divs[m].append(d)
    phis = [None] * (M + 1)
    for v in range(1, M + 1):
        if present[v]:
            phis[v] = [phi[d] for d in divs[v]]
    W = [0] * (M + 1)
    Wget = W.__getitem__
    out = []
    ans = 0
    w = 1
    for a in A:
        ds = divs[a]
        t = sum(map(mul, phis[a], map(Wget, ds))) % MOD
        ans = (2 * ans + t) % MOD
        out.append(ans)
        for d in ds:
            W[d] += w
        w = w * 2 % MOD
    sys.stdout.write("\n".join(map(str, out)) + "\n")
main()
