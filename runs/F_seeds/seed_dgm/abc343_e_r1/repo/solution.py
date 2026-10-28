import sys


def overlap(intervals):
    lo = max(s for s, _ in intervals)
    hi = min(e for _, e in intervals)
    return max(0, hi - lo)


def main():
    V1, V2, V3 = map(int, sys.stdin.read().split())
    S1 = 3 * 343
    # V1 + 2*V2 + 3*V3 must equal the total volume of the three cubes.
    if V1 + 2 * V2 + 3 * V3 != S1:
        print("No")
        return
    # Sum of pairwise intersection volumes.
    S2 = V2 + 3 * V3

    # Cube 1 fixed at [0,7] per axis; cube 2 at offset x, cube 3 at offset y per axis.
    # Per-axis option = (l12, l13, l23, l123) overlap lengths.
    R = range(-14, 15)
    opts = {}
    for x in R:
        for y in R:
            c1 = (0, 7)
            c2 = (x, x + 7)
            c3 = (y, y + 7)
            key = (overlap([c1, c2]), overlap([c1, c3]),
                   overlap([c2, c3]), overlap([c1, c2, c3]))
            if key not in opts:
                opts[key] = (x, y)
    keys = list(opts.keys())

    # Volumes are products over the three axes.
    for k1 in keys:
        for k2 in keys:
            for k3 in keys:
                if k1[3] * k2[3] * k3[3] != V3:
                    continue
                s = (k1[0] * k2[0] * k3[0] + k1[1] * k2[1] * k3[1]
                     + k1[2] * k2[2] * k3[2])
                if s != S2:
                    continue
                x1, y1 = opts[k1]
                x2, y2 = opts[k2]
                x3, y3 = opts[k3]
                print("Yes")
                print(0, 0, 0, x1, x2, x3, y1, y2, y3)
                return
    print("No")


main()
