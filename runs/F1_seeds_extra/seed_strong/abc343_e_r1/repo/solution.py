import sys


def main():
    V1, V2, V3 = map(int, sys.stdin.read().split())
    if V1 + 2 * V2 + 3 * V3 != 1029:
        print("No")
        return
    # 1D profiles: cube1 at 0, cube2 at p, cube3 at q (p, q in [-7, 7]).
    # profile = (triple, o12, o13, o23) as 1D overlap lengths.
    prof = {}
    R = range(-14, 15)
    for p in R:
        for q in R:
            a = (0, p, q)
            t = max(0, min(a) + 7 - max(a))
            o12 = max(0, 7 - abs(a[0] - a[1]))
            o13 = max(0, 7 - abs(a[0] - a[2]))
            o23 = max(0, 7 - abs(a[1] - a[2]))
            key = (t, o12, o13, o23)
            if key not in prof:
                prof[key] = (p, q)
    profs = list(prof.items())
    P_target = V2 + 3 * V3
    for kx, (px, qx) in profs:
        tx, x12, x13, x23 = kx
        for ky, (py, qy) in profs:
            ty, y12, y13, y23 = ky
            txy = tx * ty
            c12 = x12 * y12
            c13 = x13 * y13
            c23 = x23 * y23
            for kz, (pz, qz) in profs:
                tz, z12, z13, z23 = kz
                if txy * tz != V3:
                    continue
                if c12 * z12 + c13 * z13 + c23 * z23 != P_target:
                    continue
                print("Yes")
                print(0, 0, 0, px, py, pz, qx, qy, qz)
                return
    print("No")


main()
