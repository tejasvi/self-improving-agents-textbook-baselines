import sys

def main():
    V1, V2, V3 = map(int, sys.stdin.read().split())
    if V1 + 2 * V2 + 3 * V3 != 3 * 343:
        print("No")
        return
    # Per-axis tuples: (t, p12, p13, p23) for offsets o2, o3 with cube1 at 0.
    def ov(lo1, hi1, lo2, hi2):
        return max(0, min(hi1, hi2) - max(lo1, lo2))
    axis = set()
    R = range(-21, 22)
    for o2 in R:
        for o3 in R:
            lo = [0, o2, o3]
            hi = [7, o2 + 7, o3 + 7]
            t = max(0, min(hi) - max(lo))
            p12 = ov(lo[0], hi[0], lo[1], hi[1])
            p13 = ov(lo[0], hi[0], lo[2], hi[2])
            p23 = ov(lo[1], hi[1], lo[2], hi[2])
            axis.add((t, p12, p13, p23, o2, o3))
    # Combine x and y, dedupe by (T, q12, q13, q23), keep offsets for reconstruction.
    xy = {}
    for (t1, a12, a13, a23, x2, x3) in axis:
        for (t2, b12, b13, b23, y2, y3) in axis:
            key = (t1 * t2, a12 * b12, a13 * b13, a23 * b23)
            if key not in xy:
                xy[key] = (x2, x3, y2, y3)
    for (t3, c12, c13, c23, z2, z3) in axis:
        for key, offs in xy.items():
            T, q12, q13, q23 = key
            if T * t3 == V3 and q12 * c12 + q13 * c13 + q23 * c23 == V2 + 3 * V3:
                x2, x3, y2, y3 = offs
                print("Yes")
                print(0, 0, 0, x2, y2, z2, x3, y3, z3)
                return
    print("No")

main()
