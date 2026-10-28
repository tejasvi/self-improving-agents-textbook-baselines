import sys
from operator import mul, itemgetter

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
            for k in range(p, M + 1, p):
                phi[k] -= phi[k] // p

    # divisor lists only for values that appear
    present = [False] * (M + 1)
    for a in A:
        present[a] = True
    divs = [None] * (M + 1)
    for d in range(1, M + 1):
        for k in range(d, M + 1, d):
            if present[k]:
                if divs[k] is None:
                    divs[k] = []
                divs[k].append(d)

    C = [0] * (M + 1)
    out = []
    R = 0
    pw = 1  # 2^{i-1} mod MOD for 1-indexed i
    for a in A:
        D = divs[a]
        if len(D) == 1:
            T = phi[1] * C[1]
            C[1] += pw
        else:
            vals = itemgetter(*D)(C)
            T = sum(map(mul, map(phi.__getitem__, D), vals))
            for d in D:
                C[d] += pw
        R = (2 * R + T) % MOD
        out.append(R)
        pw = pw * 2 % MOD
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
