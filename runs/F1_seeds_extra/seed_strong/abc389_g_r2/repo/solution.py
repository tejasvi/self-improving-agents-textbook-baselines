import sys


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    P = int(data[1])
    H = N // 2
    E = N * (N - 1) // 2
    L = E + 1  # coefficient count (degrees 0..E)
    B = 16     # bytes per slot (128 bits, enough for accumulated sums)
    SLOT_LIM = 1 << (8 * B)

    def pack(lst):
        return int.from_bytes(b''.join(c.to_bytes(B, 'little') for c in lst), 'little')

    def unpack(x):
        # returns list of L coefficients reduced mod P
        nbytes = B * L
        bs = x.to_bytes(max(nbytes, (x.bit_length() + 7) // 8), 'little')
        return [int.from_bytes(bs[i * B:(i + 1) * B], 'little') % P for i in range(L)]

    def reduce_(x):
        return pack(unpack(x))

    MAXD = N
    C = [[0] * (MAXD + 1) for _ in range(MAXD + 1)]  # exact small binomials mod P
    for m in range(MAXD + 1):
        C[m][0] = 1 % P
        for k in range(1, m + 1):
            C[m][k] = (C[m - 1][k - 1] + C[m - 1][k]) % P

    # (1+y)^m as packed poly, for m up to E
    ROW_CACHE = {}

    def row(m):
        if m not in ROW_CACHE:
            # exact binomial coefficients of (1+y)^m mod P
            from math import comb
            coeffs = [comb(m, k) % P for k in range(m + 1)]
            ROW_CACHE[m] = pack(coeffs)
        return ROW_CACHE[m]

    # Wp[s][t] = ((1+y)^s - 1)^t * (1+y)^{C(t,2)} mod P, packed
    def W(s, t):
        acc = 0
        for j in range(t + 1):
            coef = C[t][j]
            if (t - j) & 1:
                coef = (P - coef) % P
            if coef == 0:
                continue
            m = s * j + t * (t - 1) // 2
            acc += row(m) * coef
        return reduce_(acc)

    Wp = [[0] * (H + 1) for _ in range(H + 1)]
    for s in range(1, H + 1):
        for t in range(1, H + 1):
            Wp[s][t] = W(s, t)

    # dp[u]: dict state(e,o,s,p) -> packed poly (accumulated, unreduced)
    # state meaning: e even-layer vertices, o odd-layer vertices, last layer size s, parity p of last layer.
    # Start: layer 0 = {vertex 1}, size 1, parity 0.
    dp = [dict() for _ in range(N + 1)]
    dp[1][(1, 0, 1, 0)] = pack([1] + [0] * (L - 1))
    final = 0
    for u in range(1, N + 1):
        cur = dp[u]
        dp[u] = None
        for st, acc in cur.items():
            e, o, s, p = st
            if e == H and o == H:
                final += acc
                continue
            v = acc
            # reduce source to keep sizes bounded
            v = reduce_(v)
            q = 1 - p
            remain = N - 1 - u  # unlabeled vertices not yet used, excluding vertex 1 already counted in u
            for t in range(1, N - u + 1):
                if q == 0:
                    ne, no = e + t, o
                else:
                    ne, no = e, o + t
                if ne > H or no > H:
                    break
                # choose t labeled vertices from the N-u unused vertices
                binom = comb_mod(N - u, t, P)
                if binom == 0:
                    continue
                term = (v * Wp[s][t]) * binom
                key = (ne, no, t, q)
                nu = u + t
                d = dp[nu]
                d[key] = d.get(key, 0) + term
        if u == N:
            break
    final = reduce_(final)
    coeffs = unpack(final)
    out = [str(coeffs[M] % P) for M in range(N - 1, E + 1)]
    print(" ".join(out))


def comb_mod(n, k, P):
    if k < 0 or k > n:
        return 0
    from math import comb
    return comb(n, k) % P


main()
