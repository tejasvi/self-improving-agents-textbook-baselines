import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    cubes = []
    idx = 1
    for _ in range(n):
        x1, y1, z1, x2, y2, z2 = (int(v) for v in data[idx:idx + 6])
        idx += 6
        cubes.append(((x1, y1, z1), (x2, y2, z2)))

    S = 101 * 10000
    nb = [set() for _ in range(n)]

    for a in range(3):
        b = (a + 1) % 3
        c = (a + 2) % 3
        minus = [-1] * S  # cells of min faces: index p*10000 + y*100 + z
        plus = [-1] * S   # cells of max faces
        for i, (lo, hi) in enumerate(cubes):
            pl = lo[a] * 10000
            ph = hi[a] * 10000
            zl, zh = lo[c], hi[c]
            for y in range(lo[b], hi[b]):
                base = y * 100
                s = base + zl
                e = base + zh
                minus[pl + s:pl + e] = [i] * (zh - zl)
                plus[ph + s:ph + e] = [i] * (zh - zl)
        # lookups: plus face of i against min faces at same plane, and vice versa
        for i, (lo, hi) in enumerate(cubes):
            zl, zh = lo[c], hi[c]
            ph = hi[a] * 10000
            pl = lo[a] * 10000
            s_ = nb[i]
            for y in range(lo[b], hi[b]):
                base = y * 100
                s = base + zl
                e = base + zh
                s_.update(minus[ph + s:ph + e])
                s_.update(plus[pl + s:pl + e])
            s_.discard(-1)
            s_.discard(i)

    out = [str(len(s)) for s in nb]
    sys.stdout.write("\n".join(out) + "\n")


main()
