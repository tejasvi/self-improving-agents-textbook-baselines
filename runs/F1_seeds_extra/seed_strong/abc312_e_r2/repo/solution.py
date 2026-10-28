import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    cubes = []
    pos = 1
    for _ in range(n):
        vals = [int(v) for v in data[pos:pos + 6]]
        pos += 6
        lo = vals[0:3]
        hi = vals[3:6]
        cubes.append((lo, hi))

    # minF[a][c]: grid over the two other axes, owner (1-based id) of cells
    # of cuboids whose lo[a] == c. maxF[a][c]: cuboids whose hi[a] == c.
    minF = [dict() for _ in range(3)]
    maxF = [dict() for _ in range(3)]

    def get_grid(d, key):
        g = d.get(key)
        if g is None:
            g = [[0] * 101 for _ in range(101)]
            d[key] = g
        return g

    axes_other = [(1, 2), (0, 2), (0, 1)]
    for i, (lo, hi) in enumerate(cubes):
        idv = i + 1
        for a in range(3):
            p, q = axes_other[a]
            wq = hi[q] - lo[q]
            fill = [idv] * wq
            g = get_grid(minF[a], lo[a])
            for r in range(lo[p], hi[p]):
                g[r][lo[q]:hi[q]] = fill
            g = get_grid(maxF[a], hi[a])
            for r in range(lo[p], hi[p]):
                g[r][lo[q]:hi[q]] = fill

    res = [0] * n
    for i, (lo, hi) in enumerate(cubes):
        s = set()
        for a in range(3):
            p, q = axes_other[a]
            # min face of i at plane lo[a]: look at maxF cells on the left side
            g = maxF[a].get(lo[a])
            if g is not None:
                for r in range(lo[p], hi[p]):
                    s.update(g[r][lo[q]:hi[q]])
            # max face of i at plane hi[a]: look at minF cells on the right side
            g = minF[a].get(hi[a])
            if g is not None:
                for r in range(lo[p], hi[p]):
                    s.update(g[r][lo[q]:hi[q]])
        s.discard(0)
        s.discard(i + 1)
        res[i] = len(s)

    sys.stdout.write("\n".join(map(str, res)) + "\n")


main()
