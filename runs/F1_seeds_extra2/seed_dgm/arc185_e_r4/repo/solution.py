import sys
from operator import mul

MOD = 998244353


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    M = max(A)

    # Euler phi sieve
    phi = list(range(M + 1))
    for p in range(2, M + 1):
        if phi[p] == p:
            for q in range(p, M + 1, p):
                phi[q] -= phi[q] // p

    # Divisor lists only for values that occur
    needed = set(A)
    divs_of = {}
    for a in needed:
        ds = []
        d = 1
        while d * d <= a:
            if a % d == 0:
                ds.append(d)
                if d * d != a:
                    ds.append(a // d)
            d += 1
        divs_of[a] = (tuple(ds), tuple(phi[d] for d in ds))

    # T[d] = sum over earlier i with d | A_i of 2^{i-1} mod MOD
    T = [0] * (M + 1)
    out = []
    ans = 0
    p2 = 1
    for a in A:
        D, PH = divs_of[a]
        s = sum(map(mul, PH, map(T.__getitem__, D)))
        ans = (2 * ans + s) % MOD
        out.append(ans)
        for d in D:
            T[d] = (T[d] + p2) % MOD
        p2 = p2 * 2 % MOD
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
