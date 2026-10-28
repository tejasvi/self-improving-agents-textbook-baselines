import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    T = int(data[pos]); pos += 1
    out = []
    SH = 20
    S = 1 << SH          # key = value * S + count  (count < S)
    NEG = -(1 << 300)
    for _ in range(T):
        n = int(data[pos]); k = int(data[pos + 1]); pos += 2
        rows = []
        for i in range(n):
            x = int(data[pos]); y = int(data[pos + 1]); z = int(data[pos + 2])
            pos += 3
            rows.append((2 * x, 2 * y, 2 * z))
        m = 2 * k

        def run(lam):
            # Maximise sum over chosen cakes of (2*label_value - lam), where the
            # label of each chosen cake is X, Y or Z and each label is used an
            # even number of times. Ties broken by larger count (low bits).
            # State s (3 bits) = parity of usage of labels X,Y,Z; choosing a
            # cake with label t flips bit t, so f'[s] = max(f[s], f[s^t]+a_t).
            f0 = 0; f1 = NEG; f2 = NEG; f3 = NEG
            f4 = NEG; f5 = NEG; f6 = NEG; f7 = NEG
            for x, y, z in rows:
                a0 = (x - lam) * S + 1
                a1 = (y - lam) * S + 1
                a2 = (z - lam) * S + 1
                n0 = max(f0, f1 + a0, f2 + a1, f4 + a2)
                n1 = max(f1, f0 + a0, f3 + a1, f5 + a2)
                n2 = max(f2, f3 + a0, f0 + a1, f6 + a2)
                n3 = max(f3, f2 + a0, f1 + a1, f7 + a2)
                n4 = max(f4, f5 + a0, f6 + a1, f0 + a2)
                n5 = max(f5, f4 + a0, f7 + a1, f1 + a2)
                n6 = max(f6, f7 + a0, f4 + a1, f2 + a2)
                n7 = max(f7, f6 + a0, f5 + a1, f3 + a2)
                f0, f1, f2, f3, f4, f5, f6, f7 = n0, n1, n2, n3, n4, n5, n6, n7
            return f0

        # Largest penalty lam (doubled units) whose optimal count is >= m.
        # Marginal values lie in [0, 4e9], so this range is sufficient.
        lo, hi = -1, 4 * 10 ** 9 + 2
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if run(mid) % S >= m:
                lo = mid
            else:
                hi = mid - 1
        key = run(lo)
        val = key // S
        out.append(str((val + lo * m) // 2))
    sys.stdout.write("\n".join(out) + "\n")


main()
