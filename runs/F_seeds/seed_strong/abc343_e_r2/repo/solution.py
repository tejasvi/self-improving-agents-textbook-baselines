import sys


def main():
    data = sys.stdin.read().split()
    V1, V2, V3 = int(data[0]), int(data[1]), int(data[2])
    S = 7
    if V1 + 2 * V2 + 3 * V3 != 3 * S ** 3:
        print("No")
        return

    # 1D analysis: cube1 at 0, cube2 at u, cube3 at v.
    # Each axis yields (p12, p13, p23, t) = 1D overlap lengths.
    witness = {}
    R = range(-2 * S, 2 * S + 1)
    for u in R:
        for v in R:
            lo12, hi12 = max(0, u), min(S, u + S)
            lo13, hi13 = max(0, v), min(S, v + S)
            lo23, hi23 = max(u, v), min(u, v) + S
            p12 = max(0, hi12 - lo12)
            p13 = max(0, hi13 - lo13)
            p23 = max(0, hi23 - lo23)
            t = max(0, min(S, u + S, v + S) - max(0, u, v))
            key = (p12, p13, p23, t)
            if key not in witness:
                witness[key] = (u, v)

    keys = list(witness.keys())
    for kx in keys:
        ax12, ax13, ax23, axt = kx
        for ky in keys:
            ay12, ay13, ay23, ayt = ky
            t_xy = axt * ayt
            # need t_xy * tz == V3
            for kz in keys:
                az12, az13, az23, azt = kz
                if t_xy * azt != V3:
                    continue
                I12 = ax12 * ay12 * az12
                I13 = ax13 * ay13 * az13
                I23 = ax23 * ay23 * az23
                if I12 + I13 + I23 - 3 * V3 == V2:
                    ux, vx = witness[kx]
                    uy, vy = witness[ky]
                    uz, vz = witness[kz]
                    # cube1 at (0,0,0); cube2 at (ux,uy,uz); cube3 at (vx,vy,vz)
                    print("Yes")
                    print(0, 0, 0, ux, uy, uz, vx, vy, vz)
                    return
    print("No")


main()
