import sys
from operator import itemgetter, mul


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    MOD = 998244353
    M = max(A)

    # Euler phi sieve
    phi = list(range(M + 1))
    for p in range(2, M + 1):
        if phi[p] == p:
            for k in range(p, M + 1, p):
                phi[k] -= phi[k] // p

    # Divisor lists for values that occur
    needed = set(A)
    divs = {v: [] for v in needed}
    for d in range(1, M + 1):
        for m in range(d, M + 1, d):
            lst = divs.get(m)
            if lst is not None:
                lst.append(d)

    # Per value: precomputed getter for T over divisors, and phi weights
    getters = {}
    phiw = {}
    for v, lst in divs.items():
        getters[v] = itemgetter(*lst) if len(lst) > 1 else (lambda T, d=lst[0]: (T[d],))
        phiw[v] = [phi[d] for d in lst]

    T = [0] * (M + 1)
    out = []
    ans = 0
    w = 1  # 2^(j) mod MOD for index j (0-based)
    for a in A:
        ds = divs[a]
        vals = getters[a](T)
        S = sum(map(mul, phiw[a], vals)) % MOD
        ans = (2 * ans + S) % MOD
        out.append(ans)
        for d in ds:
            T[d] += w
        w = w * 2 % MOD
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
