import sys
from math import comb


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    P = int(data[1])
    half = N // 2
    KMAX = comb(N, 2)
    K = KMAX + 1

    B = [[comb(a, b) % P for b in range(N + 1)] for a in range(N + 1)]

    # states[v]: dict (e, s, p) -> poly (list of length K, coefficients in y=1+x)
    # e: vertices at even distance so far, s: size of last layer,
    # p: parity of the index of the next layer (1 = odd, 0 = even)
    states = [dict() for _ in range(N + 1)]
    init = [0] * K
    init[0] = 1
    states[1][(1, 1, 1)] = init

    final = [0] * K
    for v in range(1, N + 1):
        cur = states[v]
        states[v] = None
        for (e, s, p), vec in cur.items():
            if v == N:
                if e == half:
                    for k in range(K):
                        if vec[k]:
                            final[k] = (final[k] + vec[k]) % P
                continue
            rem = N - v
            # Z = vec * (y^s - 1)^t, built incrementally over t
            Z = vec
            for t in range(1, rem + 1):
                # multiply Z by (y^s - 1); degree after v+t vertices <= C(v+t,2)
                L = min(K, comb(v + t, 2) + 1)
                if len(Z) < L:
                    Z = Z + [0] * (L - len(Z))
                if s < L:
                    Z = [((Z[k - s] if k >= s else 0) - Z[k]) % P for k in range(L)]
                else:
                    Z = [(-Z[k]) % P for k in range(L)]
                ne = e + t if p == 0 else e
                if ne > half:
                    # e only grows with t, so larger t also invalid when p == 0
                    if p == 0:
                        break
                    continue
                w = B[rem][t]
                sh = comb(t, 2)
                if sh >= K:
                    continue
                key = (ne, t, 1 - p)
                tgt = states[v + t].get(key)
                if tgt is None:
                    tgt = [0] * K
                    states[v + t][key] = tgt
                seg = tgt[sh:sh + len(Z)]
                tgt[sh:sh + len(seg)] = [(a + w * z) % P for a, z in zip(seg, Z)]

    out = []
    for M in range(N - 1, KMAX + 1):
        total = 0
        for k in range(M, K):
            c = final[k]
            if c:
                total += c * comb(k, M)
        out.append(total % P)
    print(" ".join(map(str, out)))


main()
