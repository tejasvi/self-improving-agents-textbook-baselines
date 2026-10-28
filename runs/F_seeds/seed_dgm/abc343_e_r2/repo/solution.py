import sys


def main():
    V1, V2, V3 = map(int, sys.stdin.read().split())
    # Each cube has volume 343; V1 + 2*V2 + 3*V3 = 3*343.
    if V1 + 2 * V2 + 3 * V3 != 3 * 343:
        print("No")
        return

    # Per-axis signature with cube1 at 0, cube2 at a2, cube3 at a3.
    # Overlap of two 1D intervals [x, x+7] is max(0, min(hi)-max(lo)).
    # Positions in [-14, 14] suffice since gaps > 7 are equivalent to 8.
    sigs = {}
    R = range(-14, 15)
    for a2 in R:
        for a3 in R:
            s = [0, a2, a3]
            lo = s
            hi = [x + 7 for x in s]

            def ov(i, j):
                return max(0, min(hi[i], hi[j]) - max(lo[i], lo[j]))

            t = max(0, min(hi) - max(lo))
            key = (t, ov(0, 1), ov(0, 2), ov(1, 2))
            if key not in sigs:
                sigs[key] = (a2, a3)

    keys = list(sigs.keys())
    target_p = V2 + 3 * V3  # sum of pairwise intersection volumes
    for k1 in keys:
        for k2 in keys:
            # prune on triple product early
            t12 = k1[0] * k2[0]
            for k3 in keys:
                if t12 * k3[0] != V3:
                    continue
                P = (k1[1] * k2[1] * k3[1] + k1[2] * k2[2] * k3[2]
                     + k1[3] * k2[3] * k3[3])
                if P != target_p:
                    continue
                if 1029 - 2 * P + 3 * V3 != V1:
                    continue
                pos = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                for axis, k in enumerate((k1, k2, k3)):
                    a2, a3 = sigs[k]
                    pos[1][axis] = a2
                    pos[2][axis] = a3
                print("Yes")
                print(" ".join(str(v) for c in pos for v in c))
                return
    print("No")


main()
