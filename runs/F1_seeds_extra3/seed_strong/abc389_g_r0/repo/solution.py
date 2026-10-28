import sys
from math import comb
from operator import mul, add


def main():
    N, P = map(int, sys.stdin.read().split())
    MAXE = N * (N - 1) // 2
    D = MAXE + 1  # polynomial degree <= MAXE; we evaluate at D points
    xs = list(range(D))
    # z = 1 + x evaluated at points
    zv = [(1 + x) % P for x in xs]
    # zp[k] = z^k at all points, k up to MAXE
    zp = [[1] * D]
    for k in range(1, max(MAXE, N) + 1):
        prev = zp[-1]
        zp.append([a * b % P for a, b in zip(prev, zv)])
    # W[t][s] = z^{C(s,2)} * (z^t - 1)^s  (vector over points)
    W = [[None] * (N + 1) for _ in range(N + 1)]
    for t in range(1, N + 1):
        Bt = [(a - 1) % P for a in zp[t]]
        cur = [1] * D
        for s in range(1, N + 1):
            cur = [a * b % P for a, b in zip(cur, Bt)]
            c = zp[s * (s - 1) // 2]
            W[t][s] = [a * b % P for a, b in zip(cur, c)]

    half = N // 2
    W2 = [None] * (N + 1)
    for v in range(1, N + 1):
        W2[v] = [[None] * (N + 1) for _ in range(N + 1)]
        for t in range(1, N + 1):
            for s in range(1, N - v + 1):
                c = comb(N - v, s) % P
                W2[v][t][s] = [a * c % P for a in W[t][s]]
    # dp[(v, t, e, p)] -> list over points; v vertices placed, last layer size t,
    # e = #vertices in even layers so far, p = parity of last layer index
    dp = {(1, 1, 1, 0): [1] * D}
    # group by v for ordered processing
    by_v = [dict() for _ in range(N + 1)]
    by_v[1][(1, 1, 0)] = [1] * D  # key (t, e, p)
    result = [0] * D
    for v in range(1, N + 1):
        cur = by_v[v]
        for (t, e, p), vec in cur.items():
            vec = [a % P for a in vec]
            if v == N:
                if e == half:
                    result = [(r + a) % P for r, a in zip(result, vec)]
                continue
            np_ = 1 - p
            for s in range(1, N - v + 1):
                ne = e + (s if np_ == 0 else 0)
                if ne > half:
                    continue
                w = W2[v][t][s]
                nvec = list(map(mul, vec, w))
                tgt = by_v[v + s]
                key = (s, ne, np_)
                if key in tgt:
                    tgt[key] = list(map(add, tgt[key], nvec))
                else:
                    tgt[key] = nvec
        by_v[v] = None
    # result[k] = value of edge polynomial at point k
    ys = result
    # Newton-free: Lagrange interpolation to coefficients
    full = [1]
    for j in xs:
        new = [0] * (len(full) + 1)
        for i, c in enumerate(full):
            new[i + 1] = (new[i + 1] + c) % P
            new[i] = (new[i] - c * j) % P
        full = new
    coeffs = [0] * D
    for j in xs:
        if ys[j] == 0:
            continue
        q = [0] * D
        carry = 0
        for i in range(D, 0, -1):
            carry = (full[i] + carry * j) % P
            q[i - 1] = carry
        denom = 1
        for k in xs:
            if k != j:
                denom = denom * (j - k) % P
        f = ys[j] * pow(denom, P - 2, P) % P
        for i in range(D):
            coeffs[i] = (coeffs[i] + q[i] * f) % P
    out = [str(coeffs[m]) for m in range(N - 1, MAXE + 1)]
    print(" ".join(out))


main()
