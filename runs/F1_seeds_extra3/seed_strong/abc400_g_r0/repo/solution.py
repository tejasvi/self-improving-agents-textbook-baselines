import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    T = int(data[pos]); pos += 1
    SH = 17
    MASK = (1 << SH) - 1
    out = []

    for _ in range(T):
        n = int(data[pos]); k = int(data[pos + 1]); pos += 2
        xs = [0] * n
        ys = [0] * n
        zs = [0] * n
        for i in range(n):
            xs[i] = 2 * int(data[pos]);
            ys[i] = 2 * int(data[pos + 1]);
            zs[i] = 2 * int(data[pos + 2])
            pos += 3
        cakes = list(zip(xs, ys, zs))
        m = 2 * k

        # run(D, N): maximise sum over chosen cakes of (D*w - N) where w = 2v.
        # Returns (V, c): optimal value and largest count among optima.
        def run(D, N):
            NEG = -(1 << 120)
            d0, d1, d2, d3, d4, d5, d6, d7 = 0, NEG, NEG, NEG, NEG, NEG, NEG, NEG
            for x, y, z in cakes:
                w0 = ((D * x - N) << SH) + 1
                w1 = ((D * y - N) << SH) + 1
                w2 = ((D * z - N) << SH) + 1
                # new[p] = max(old[p], old[p^1]+w0, old[p^2]+w1, old[p^4]+w2)
                n0 = max(d0, d1 + w0, d2 + w1, d4 + w2)
                n1 = max(d1, d0 + w0, d3 + w1, d5 + w2)
                n2 = max(d2, d3 + w0, d0 + w1, d6 + w2)
                n3 = max(d3, d2 + w0, d1 + w1, d7 + w2)
                n4 = max(d4, d5 + w0, d6 + w1, d0 + w2)
                n5 = max(d5, d4 + w0, d7 + w1, d1 + w2)
                n6 = max(d6, d7 + w0, d4 + w1, d2 + w2)
                n7 = max(d7, d6 + w0, d5 + w1, d3 + w2)
                d0, d1, d2, d3, d4, d5, d6, d7 = n0, n1, n2, n3, n4, n5, n6, n7
            dp = [d0, d1, d2, d3, d4, d5, d6, d7]
            r = dp[0]
            return (r >> SH), (r & MASK)

        # Points on the concave curve G(c) (c = cake count, G = sum of 2v).
        BIG = 10 ** 13
        # A: count 0, G=0 (any nu large enough makes everything negative)
        Ac, AG = 0, 0
        # B: maximal count, nu = -BIG forces count to be maximal
        V, c = run(1, -BIG)
        Bc, BG = c, V - BIG * c
        ans = None
        if m == Bc:
            ans = BG
        elif m == Ac:
            ans = AG
        else:
            while True:
                D = Bc - Ac
                N = BG - AG
                V, c = run(D, N)
                base = D * AG - N * Ac
                if V <= base:
                    # chord is exact on [Ac, Bc]
                    ans = (D * AG + (m - Ac) * N) // D
                    break
                G_new = (V + N * c) // D
                if c == m:
                    ans = G_new
                    break
                if c < m:
                    Ac, AG = c, G_new
                else:
                    Bc, BG = c, G_new
        out.append(str(ans // 2))
    sys.stdout.write("\n".join(out) + "\n")


main()
