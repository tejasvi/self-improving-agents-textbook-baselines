import sys
from math import comb


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    P = int(data[1])
    E = N * (N - 1) // 2
    L = E + 2                      # slots per packed polynomial
    W = 128                        # bits per slot
    half = N // 2

    def pack(coeffs):
        v = 0
        for c in reversed(coeffs):
            v = (v << W) | (c % P)
        return v

    def unpack_mod(X):
        if X == 0:
            return 0
        nslots = X.bit_length() // W + 1
        b = X.to_bytes(nslots * 16, 'little')
        coeffs = [int.from_bytes(b[i * 16:(i + 1) * 16], 'little') % P
                  for i in range(nslots)]
        return pack(coeffs)

    # poly helpers (exact integers)
    def polymul(p, q):
        r = [0] * (len(p) + len(q) - 1)
        for i, x in enumerate(p):
            if x == 0:
                continue
            for j, y in enumerate(q):
                r[i + j] += x * y
        return r

    def binom_poly(k):  # (1+x)^k
        return [comb(k, i) for i in range(k + 1)]

    # T[a][b] = (1+x)^{C(b,2)} * ((1+x)^a - 1)^b, packed mod P
    T = {}
    for a in range(1, N + 1):
        base = binom_poly(a)
        base[0] -= 1  # (1+x)^a - 1
        powp = [1]
        for b in range(1, N + 1):
            powp = polymul(powp, base)
            if a + b > N:
                break
            poly = polymul(powp, binom_poly(comb(b, 2)))
            T[(a, b)] = pack(poly)

    # F[(s, a, e, p)] = packed polynomial
    bys = [dict() for _ in range(N + 1)]
    bys[1][(1, 1, 0)] = 1  # key (a, e, p) -> packed
    for s in range(1, N + 1):
        cur = bys[s]
        for (a, e, p), X in cur.items():
            if X == 0:
                continue
            X = unpack_mod(X)
            rem = N - s
            for b in range(1, rem + 1):
                ne = e + (b if p == 1 else 0)
                o = (s + b) - ne
                if ne > half or o > half:
                    continue
                c = comb(rem, b) % P
                t = T.get((a, b))
                if t is None:
                    continue
                prod = X * t * c
                key = (b, ne, 1 - p)
                d = bys[s + b]
                d[key] = d.get(key, 0) + prod
    # final: s = N, e = half
    fin = bys[N]
    acc = 0
    for (a, e, p), X in fin.items():
        if e != half:
            continue
        acc += X
    acc = unpack_mod(acc)
    coeffs = [0] * (E + 1)
    if acc:
        b = acc.to_bytes(((acc.bit_length() // W) + 1) * 16, 'little')
        for i in range(min(E + 1, len(b) // 16)):
            coeffs[i] = int.from_bytes(b[i * 16:(i + 1) * 16], 'little') % P
    out = []
    for M in range(N - 1, E + 1):
        out.append(coeffs[M])
    print(' '.join(map(str, out)))


main()
