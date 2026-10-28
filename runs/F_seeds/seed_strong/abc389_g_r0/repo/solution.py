import sys


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    P = int(data[1])
    H = N // 2
    D = N * (N - 1) // 2
    npts = D + 1

    C = [[0] * (N + 1) for _ in range(N + 1)]
    for i in range(N + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = C[i - 1][j - 1] + C[i - 1][j]

    # pw[e][k] = (1+y_k)^e mod P, y_k = k, for e up to D
    base = [(1 + y) % P for y in range(npts)]
    pw = [[1] * npts]
    for e in range(1, D + 1):
        prev = pw[-1]
        pw.append([prev[k] * base[k] % P for k in range(npts)])

    # G[(s,t)] = ((1+y)^s - 1)^t * (1+y)^{C(t,2)} pointwise, s,t <= H
    G = {}
    for s in range(1, H + 1):
        a = [(pw[s][k] - 1) % P for k in range(npts)]
        apow = [1] * npts
        for t in range(1, H + 1):
            apow = [apow[k] * a[k] % P for k in range(npts)]
            e = t * (t - 1) // 2
            G[(s, t)] = [apow[k] * pw[e][k] % P for k in range(npts)]

    # buckets[used][(E,O,s,par)] = pointwise value vector
    # par: parity of the last layer (0 = even distance, 1 = odd)
    buckets = [dict() for _ in range(N + 1)]
    buckets[1][(1, 0, 1, 0)] = [1] * npts
    for used in range(1, N):
        R = N - used
        for key, vec in buckets[used].items():
            E, O, s, par = key
            for t in range(1, R + 1):
                if par == 0:
                    if O + t > H:
                        break
                    nk = (E, O + t, t, 1)
                else:
                    if E + t > H:
                        break
                    nk = (E + t, O, t, 0)
                c = C[R][t] % P
                w = G[(s, t)]
                contrib = [vec[k] * w[k] % P * c % P for k in range(npts)]
                nb = buckets[used + t]
                if nk in nb:
                    old = nb[nk]
                    nb[nk] = [(old[k] + contrib[k]) % P for k in range(npts)]
                else:
                    nb[nk] = contrib

    vals = [0] * npts
    for key, v in buckets[N].items():
        if key[0] == H and key[1] == H:
            vals = [(vals[k] + v[k]) % P for k in range(npts)]

    # interpolation from points 0..D
    n = npts
    Q = [1]
    for j in range(n):
        newQ = [0] * (len(Q) + 1)
        for i, c in enumerate(Q):
            newQ[i + 1] = (newQ[i + 1] + c) % P
            newQ[i] = (newQ[i] - c * j) % P
        Q = newQ
    coeffs = [0] * n
    for j in range(n):
        if vals[j] == 0:
            continue
        q = [0] * n
        acc = 0
        for i in range(n, 0, -1):
            acc = (Q[i] + acc * j) % P
            q[i - 1] = acc
        denom = 1
        for k in range(n):
            if k != j:
                denom = denom * (j - k) % P
        scale = vals[j] * pow(denom, P - 2, P) % P
        for i in range(n):
            coeffs[i] = (coeffs[i] + scale * q[i]) % P

    out = [str(coeffs[M] % P) for M in range(N - 1, D + 1)]
    print(" ".join(out))


main()
