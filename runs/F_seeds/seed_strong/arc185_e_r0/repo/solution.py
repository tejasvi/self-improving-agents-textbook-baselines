import sys
from operator import itemgetter, mul, add
from itertools import repeat

MOD = 998244353


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    M = max(A)

    phi = list(range(M + 1))
    for p in range(2, M + 1):
        if phi[p] == p:
            for q in range(p, M + 1, p):
                phi[q] -= phi[q] // p

    distinct = set(A)
    divs = {v: [] for v in distinct}
    for d in range(1, M + 1):
        for q in range(d, M + 1, d):
            if q in divs:
                divs[q].append(d)

    # F[d] = sum of w_i over earlier i with d | A_i
    # gcd(A_i, A_j) = sum_{d | both} phi(d)  =>  T_j = sum_{d|A_j} phi(d) * F[d]
    F = [0] * (M + 1)
    info = {}
    for v in distinct:
        D = divs[v]
        info[v] = (D, itemgetter(*D) if len(D) > 1 else None,
                   [phi[d] for d in D])

    out = []
    ans = 0
    w = 1
    for v in A:
        D, g, ph = info[v]
        if g is not None:
            vals = g(F)
            T = sum(map(mul, ph, vals))
            list(map(F.__setitem__, D, map(add, vals, repeat(w))))
        else:
            T = F[1]
            F[1] += w
        ans = (2 * ans + T) % MOD
        out.append(ans)
        w = w * 2 % MOD
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
