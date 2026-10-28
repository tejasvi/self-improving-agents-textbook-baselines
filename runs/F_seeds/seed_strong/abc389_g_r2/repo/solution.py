import sys


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    P = int(data[1])
    D = N * (N - 1) // 2 + 1  # number of coefficients (degrees 0..C(N,2))
    B = 128  # slot width in bits (safe for accumulated sums)
    SB = B // 8
    H = N // 2

    def pack(coeffs):
        # coeffs: list of ints in [0, P) of length <= D
        bs = b''.join(c.to_bytes(SB, 'little') for c in coeffs)
        bs += b'\x00' * (SB * (D - len(coeffs)))
        return int.from_bytes(bs, 'little')

    def unpack(v):
        bs = v.to_bytes(SB * D, 'little')
        return [int.from_bytes(bs[i * SB:(i + 1) * SB], 'little') % P for i in range(D)]

    def pmul(a, b):
        r = [0] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    r[i + j] += x * y
        return [v % P for v in r]

    # binomial coefficients mod P
    CM = D + N
    C = [[0] * (CM + 1) for _ in range(CM + 1)]
    for i in range(CM + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % P

    # (1+x)^k as coefficient list
    def onepx(k):
        return [C[k][j] for j in range(k + 1)]

    # transition weight W[s][t] = ((1+x)^s - 1)^t * (1+x)^{C(t,2)}
    W = {}
    base = {}
    for s in range(1, N + 1):
        q = onepx(s)
        q[0] = 0  # (1+x)^s - 1
        base[s] = q
    for s in range(1, N):
        pw = [1]  # ((1+x)^s-1)^0
        for t in range(1, N - s + 1):
            pw = pmul(pw, base[s])
            k = t * (t - 1) // 2
            W[(s, t)] = pack(pmul(pw, onepx(k)))

    MASK = (1 << (8 * SB * D)) - 1

    # states: dict keyed by (a, e, s, p) -> packed poly
    states = {}
    states[(1, 1, 1, 0)] = pack([1])  # layer 0: size 1, even parity
    final = 0
    for a in range(1, N + 1):
        keys = [k for k in states if k[0] == a]
        for key in keys:
            _, e, s, p = key
            val = states.pop(key)
            if a == N:
                if e == H:
                    final += val
                continue
            poly = unpack(val)
            pv = pack(poly)  # reduced representation
            q = 1 - p
            o = a - e
            for t in range(1, N - a + 1):
                if q == 0:
                    e2, o2 = e + t, o
                else:
                    e2, o2 = e, o + t
                if e2 > H or o2 > H:
                    break
                nk = (a + t, e2, t, q)
                contrib = (pv * W[(s, t)] * C[N - a][t]) & MASK
                states[nk] = states.get(nk, 0) + contrib
    final = unpack(final)
    res = []
    for M in range(N - 1, N * (N - 1) // 2 + 1):
        res.append(final[M] % P)
    print(' '.join(map(str, res)))


main()
