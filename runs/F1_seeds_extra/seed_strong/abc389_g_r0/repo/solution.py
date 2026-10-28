import sys


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    P = int(data[1])
    D = N * (N - 1) // 2
    npts = D + 1
    xs = list(range(npts))  # evaluation points (distinct mod P since npts < P)
    half = N // 2

    # T[s][s2] = ((1+x)^s - 1)^s2 * (1+x)^C(s2,2), evaluated at all points
    T = [[None] * (N + 1) for _ in range(N + 1)]
    for s in range(1, N + 1):
        for s2 in range(1, N + 1):
            if s > half or s2 > half:
                continue
            vec = []
            for x in xs:
                b = (1 + x) % P
                a = (pow(b, s, P) - 1) % P
                vec.append(pow(a, s2, P) * pow(b, s2 * (s2 - 1) // 2, P) % P)
            T[s][s2] = vec

    comb = [[0] * (N + 1) for _ in range(N + 1)]
    for i in range(N + 1):
        comb[i][0] = 1
        for j in range(1, i + 1):
            comb[i][j] = comb[i - 1][j - 1] + comb[i - 1][j]
    zero = [0] * npts
    # state: (t, e, s, p) -> vector ; t vertices used, e even-level vertices,
    # s size of last layer, p parity of last layer index
    by_t = [dict() for _ in range(N + 1)]
    by_t[1] = {(1, 1, 0): [1] * npts}  # key (e, last layer size, parity)
    for t in range(1, N):
        cur = by_t[t]
        for (e, s, p), vec in cur.items():
            if s > half:
                continue
            for s2 in range(1, min(half, N - t) + 1):
                np_ = 1 - p
                if np_ == 0:
                    e2 = e + s2
                else:
                    e2 = e
                o2 = (t + s2) - e2
                if e2 > half or o2 > half:
                    continue
                Tv = T[s][s2]
                key = (e2, s2, np_)
                tgt = by_t[t + s2]
                c = comb[N - t][s2]
                prod = [a * b % P * c % P for a, b in zip(vec, Tv)]
                if key in tgt:
                    old = tgt[key]
                    tgt[key] = [(a + b) % P for a, b in zip(old, prod)]
                else:
                    tgt[key] = prod
    final = None
    for (e, s, p), vec in by_t[N].items():
        if e == half:
            if final is None:
                final = vec[:]
            else:
                final = [(a + b) % P for a, b in zip(final, vec)]
    if final is None:
        final = zero[:]

    # interpolate: values at xs = 0..D -> coefficients mod P
    n = npts
    # master polynomial prod (x - x_j), coefficients low->high
    master = [1]
    for xj in xs:
        new = [0] * (len(master) + 1)
        for i, c in enumerate(master):
            new[i + 1] = (new[i + 1] + c) % P
            new[i] = (new[i] - c * xj) % P
        master = new
    coef = [0] * n
    for j in range(n):
        xj = xs[j]
        # Q = master / (x - xj) via synthetic division (high to low)
        q = [0] * n
        carry = 0
        for i in range(n, 0, -1):
            carry = (master[i] + carry * xj) % P if i < n else master[i] % P
            q[i - 1] = carry
        # denominator = Q(xj)
        den = 0
        for i in range(n - 1, -1, -1):
            den = (den * xj + q[i]) % P
        w = final[j] * pow(den, P - 2, P) % P
        if w:
            for i in range(n):
                coef[i] = (coef[i] + w * q[i]) % P
    out = [str(coef[M]) for M in range(N - 1, D + 1)]
    print(" ".join(out))


main()
