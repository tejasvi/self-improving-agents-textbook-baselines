import sys
from math import comb


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    P = int(data[1])
    H = N // 2
    D = comb(N, 2)  # max number of edges
    npts = D + 1
    xs = list(range(npts))  # evaluation points for the edge-count variable

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % P
    invfact = [pow(f, P - 2, P) for f in fact]

    # Transition weight W[(s,b)] over evaluation points:
    # ((1+x)^s - 1)^b * (1+x)^{C(b,2)} / b!
    W = {}
    for s in range(1, N):
        for b in range(1, N - s + 1):
            wv = []
            cb2 = comb(b, 2)
            for x in xs:
                y = (1 + x) % P
                base = (pow(y, s, P) - 1) % P
                wv.append(pow(base, b, P) * pow(y, cb2, P) % P * invfact[b] % P)
            W[(s, b)] = wv

    # DP over BFS layers. State: (e, o, s, p)
    #   e/o = number of vertices at even/odd distance placed so far,
    #   s = size of last layer, p = parity of the next layer (0 even, 1 odd).
    buckets = [dict() for _ in range(N + 2)]
    buckets[1][(1, 0, 1, 1)] = [1] * npts

    total = [0] * npts
    for t in range(1, N + 1):
        cur = buckets[t]
        buckets[t] = None
        for (e, o, s, p), vals in cur.items():
            if e == H and o == H:
                total = [(a + b) % P for a, b in zip(total, vals)]
                continue
            maxb = (H - e) if p == 0 else (H - o)
            for b in range(1, maxb + 1):
                nt = t + b
                if nt > N:
                    break
                wv = W[(s, b)]
                add = [v * w % P for v, w in zip(vals, wv)]
                if p == 0:
                    key = (e + b, o, b, 1)
                else:
                    key = (e, o + b, b, 0)
                tgt = buckets[nt]
                if key in tgt:
                    old = tgt[key]
                    tgt[key] = [(a + c) % P for a, c in zip(old, add)]
                else:
                    tgt[key] = add

    # total[x] = sum over graphs of x^{edges} / prod(b_i!); multiply by (N-1)!
    fN = fact[N - 1]
    vals = [v * fN % P for v in total]

    # Interpolate polynomial of degree <= D through (xs, vals) mod P (Newton).
    n = npts
    coef = vals[:]
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            d = (xs[i] - xs[i - j]) % P
            coef[i] = (coef[i] - coef[i - 1]) * pow(d, P - 2, P) % P
    # Newton form -> monomial form
    poly = [0] * n
    poly[0] = coef[n - 1]
    deg = 0
    for i in range(n - 2, -1, -1):
        new = [0] * n
        for k in range(deg + 1):
            c = poly[k]
            if c:
                new[k + 1] = (new[k + 1] + c) % P
                new[k] = (new[k] - c * xs[i]) % P
        new[0] = (new[0] + coef[i]) % P
        poly = new
        deg += 1

    out = []
    for M in range(N - 1, D + 1):
        out.append(str(poly[M] % P))
    print(" ".join(out))


main()
