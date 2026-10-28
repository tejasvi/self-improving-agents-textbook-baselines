import sys


def main():
    N, P = map(int, sys.stdin.read().split())
    H = N // 2
    D = N * (N - 1) // 2
    L = D + 1
    xs = list(range(L))  # evaluation points, distinct mod P since P > D
    onep = [(x + 1) % P for x in xs]

    def pow_vec(base, k):
        res = [1] * L
        b = base[:]
        e = k
        while e:
            if e & 1:
                res = [r * q % P for r, q in zip(res, b)]
            e >>= 1
            if e:
                b = [q * q % P for q in b]
        return res

    C = [[0] * (N + 1) for _ in range(N + 1)]
    for i in range(N + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % P

    # pw[s] = (1+x)^s
    pw = [[1] * L]
    for s in range(1, N + 1):
        pw.append([a * b % P for a, b in zip(pw[-1], onep)])

    # W[(s, t, rem)] = C(rem,t) * (1+x)^{C(t,2)} * ((1+x)^s - 1)^t
    W = {}
    for s in range(1, H + 1):
        base = [(v - 1) % P for v in pw[s]]
        cur = [1] * L
        for t in range(1, H + 1):
            cur = [a * b % P for a, b in zip(cur, base)]  # ((1+x)^s-1)^t
            inner = cur
            edgepart = pow_vec(onep, t * (t - 1) // 2)
            w = [a * b % P for a, b in zip(inner, edgepart)]
            W[(s, t)] = w

    # DP over a = number of vertices placed so far.
    # state key (e, o, s, q) -> poly values list over evaluation points
    by_a = [dict() for _ in range(N + 1)]
    by_a[1][(1, 0, 1, 1)] = [1] * L  # vertex 1 at distance 0 (even); next layer odd
    for a in range(1, N):
        rem = N - a
        for (e, o, s, q), arr in by_a[a].items():
            maxt = min((H - e) if q == 0 else (H - o), rem)
            for t in range(1, maxt + 1):
                ne, no = (e + t, o) if q == 0 else (e, o + t)
                mult = C[rem][t]
                w = W[(s, t)]
                val = [x * y % P * mult % P for x, y in zip(arr, w)]
                key = (ne, no, t, 1 - q)
                tgt = by_a[a + t]
                if key in tgt:
                    old = tgt[key]
                    tgt[key] = [(x + y) % P for x, y in zip(old, val)]
                else:
                    tgt[key] = val
    total = [0] * L
    for (e, o, s, q), arr in by_a[N].items():
        if e == H and o == H:
            total = [(x + y) % P for x, y in zip(total, arr)]

    coeffs = interpolate(total, P)
    out = [str(coeffs[M] % P) for M in range(N - 1, D + 1)]
    print(" ".join(out))


def interpolate(ys, P):
    n = len(ys)
    c = ys[:]
    # Newton divided differences at points 0..n-1
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            num = (c[i] - c[i - 1]) % P
            den = (j) % P  # xs[i]-xs[i-j] = j
            c[i] = num * pow(den, P - 2, P) % P
    poly = [0] * n
    for i in range(n - 1, -1, -1):
        new = [0] * n
        for k in range(n - 1):
            if poly[k]:
                new[k + 1] = (new[k + 1] + poly[k]) % P
        for k in range(n):
            if poly[k]:
                new[k] = (new[k] - poly[k] * i) % P
        new[0] = (new[0] + c[i]) % P
        poly = new
    return poly


if __name__ == "__main__":
    main()
