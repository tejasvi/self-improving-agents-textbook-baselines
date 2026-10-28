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

    # minGrid[a][c]: 101x101 flat owner grid of cuboids whose min coordinate on axis a is c
    # maxGrid[a][c]: same for cuboids whose max coordinate on axis a is c
    # grid index = u*101 + v where (u, v) are the other two axes' coordinates (cells)
    W = 100
    minGrid = [dict() for _ in range(3)]
    maxGrid = [dict() for _ in range(3)]
    for j, (lo, hi) in enumerate(cubes):
        for a in range(3):
            b, c_ax = [k for k in range(3) if k != a]
            # cell indices in the other two axes
            ub0, ub1 = lo[b], hi[b]
            vc0, vc1 = lo[c_ax], hi[c_ax]
            for side, plane, store in ((0, lo[a], minGrid[a]), (1, hi[a], maxGrid[a])):
                g = store.get(plane)
                if g is None:
                    g = [-1] * (W * W)
                    store[plane] = g
                for u in range(ub0, ub1):
                    base = u * W
                    for v in range(vc0, vc1):
                        g[base + v] = j

    ans = [0] * n
    for i, (lo, hi) in enumerate(cubes):
        seen = set()
        for a in range(3):
            b, c_ax = [k for k in range(3) if k != a]
            ub0, ub1 = lo[b], hi[b]
            vc0, vc1 = lo[c_ax], hi[c_ax]
            # i on the max side of plane hi[a]: neighbours with min == hi[a]
            g = minGrid[a].get(hi[a])
            if g is not None:
                for u in range(ub0, ub1):
                    base = u * W
                    for v in range(vc0, vc1):
                        o = g[base + v]
                        if o >= 0:
                            seen.add(o)
            # i on the min side of plane lo[a]: neighbours with max == lo[a]
            g = maxGrid[a].get(lo[a])
            if g is not None:
                for u in range(ub0, ub1):
                    base = u * W
                    for v in range(vc0, vc1):
                        o = g[base + v]
                        if o >= 0:
                            seen.add(o)
        seen.discard(i)
        ans[i] = len(seen)

    sys.stdout.write("\n".join(map(str, ans)) + "\n")


main()
