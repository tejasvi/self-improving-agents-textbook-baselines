import sys
from math import comb


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    P = int(data[1])
    D = N * (N - 1) // 2
    H = N // 2
    # Work in the basis y = 1+x: a graph polynomial is sum_E c_E * y^E, and
    # its x^M coefficient is sum_E c_E * C(E, M). Coefficients c_E are signed
    # and bounded by 2^132 for N <= 30, so a 256-bit slot per exponent is exact
    # and packing them into one big integer keeps the arithmetic exact.
    B = 256

    A_cache = {}

    def A(l, t):
        # y^{C(t,2)} * (y^l - 1)^t  (edges inside new layer free, each new
        # vertex must have >=1 neighbour in previous layer)
        key = (l, t)
        if key not in A_cache:
            acc = 0
            for j in range(t + 1):
                c = comb(t, j) * (1 if (t - j) % 2 == 0 else -1)
                acc += c << (B * (l * j + t * (t - 1) // 2))
            A_cache[key] = acc
        return A_cache[key]

    # dp[total] : dict (e, l, p) -> packed poly
    # e = vertices at even BFS depth, l = last layer size, p = parity of last depth.
    dp = [dict() for _ in range(N + 1)]
    dp[1][(1, 1, 0)] = 1
    for total in range(1, N):
        cur = dp[total]
        rem = N - total
        for (e, l, p), V in cur.items():
            o = total - e
            q = 1 - p
            for t in range(1, rem + 1):
                if q == 0:
                    ne = e + t
                    if ne > H:
                        break
                else:
                    ne = e
                    if o + t > H:
                        break
                key = (ne, t, q)
                d = dp[total + t]
                d[key] = d.get(key, 0) + V * (comb(rem, t) * A(l, t))
    total_V = 0
    for (e, l, p), V in dp[N].items():
        if e == H:
            total_V += V
    mask = (1 << B) - 1
    half = 1 << (B - 1)
    full = 1 << B
    cs = []
    V = total_V
    for E in range(D + 1):
        r = V & mask
        if r >= half:
            r -= full
        cs.append(r)
        V = (V - r) >> B
    out = []
    for M in range(N - 1, D + 1):
        s = 0
        for E in range(M, D + 1):
            if cs[E]:
                s += cs[E] * comb(E, M)
        out.append(s % P)
    print(" ".join(map(str, out)))


main()
