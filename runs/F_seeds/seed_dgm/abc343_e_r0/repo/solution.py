import sys

N = 7


def axis_tuples():
    """Distinct per-axis (o12, o13, o23, t) for cube positions 0, x2, x3."""
    res = {}
    rng = range(-N - 1, 2 * N + 2)
    for x2 in rng:
        for x3 in rng:
            p = (0, x2, x3)
            o12 = max(0, N - abs(x2))
            o13 = max(0, N - abs(x3))
            o23 = max(0, N - abs(x2 - x3))
            t = max(0, N - (max(p) - min(p)))
            key = (o12, o13, o23, t)
            if key not in res:
                res[key] = (x2, x3)
    return res


def main():
    V1, V2, V3 = map(int, sys.stdin.read().split())
    if V1 + 2 * V2 + 3 * V3 != 3 * N ** 3:
        print("No")
        return
    tuples = axis_tuples()
    items = list(tuples.items())
    target = V2 + 3 * V3
    for kx, px in items:
        for ky, py in items:
            # partial products
            ex = (kx[0] * ky[0], kx[1] * ky[1], kx[2] * ky[2], kx[3] * ky[3])
            for kz, pz in items:
                if ex[3] * kz[3] != V3:
                    continue
                s = (ex[0] * kz[0] + ex[1] * kz[1] + ex[2] * kz[2])
                if s != target:
                    continue
                # Found: cube1 at (0,0,0); cube2 = (x2 of each axis), cube3 = (x3 of each axis)
                a2, a3 = px[0], px[1]
                b2, b3 = py[0], py[1]
                c2, c3 = pz[0], pz[1]
                print("Yes")
                print(0, 0, 0, a2, b2, c2, a3, b3, c3)
                return
    print("No")


main()
