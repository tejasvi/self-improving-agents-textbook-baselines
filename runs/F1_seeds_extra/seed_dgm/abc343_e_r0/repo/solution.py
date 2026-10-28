import sys


def main():
    V1, V2, V3 = map(int, sys.stdin.read().split())
    N = 7
    if V1 + 2 * V2 + 3 * V3 != 3 * N ** 3:
        print("No")
        return

    # Per-dimension signatures: (p12, p13, p23, t) -> offsets (a2, a3), with a1 = 0.
    # Offsets can be normalized into [0, 14] (gaps > 7 never matter).
    sig = {}
    R = range(0, 2 * N + 1)
    for b in R:
        for c in R:
            p12 = max(0, N - abs(b))
            p13 = max(0, N - abs(c))
            p23 = max(0, N - abs(b - c))
            t = max(0, min(0, b, c) + N - max(0, b, c))
            key = (p12, p13, p23, t)
            if key not in sig:
                sig[key] = (0, b, c)
    items = list(sig.items())

    for k1, o1 in items:
        for k2, o2 in items:
            for k3, o3 in items:
                # Pairwise intersections and triple intersection
                I12 = k1[0] * k2[0] * k3[0]
                I13 = k1[1] * k2[1] * k3[1]
                I23 = k1[2] * k2[2] * k3[2]
                T = k1[3] * k2[3] * k3[3]
                P = I12 + I13 + I23
                E2 = P - 3 * T
                E1 = 3 * N ** 3 - 2 * P + 3 * T
                if E1 == V1 and E2 == V2 and T == V3:
                    # cube i (0-based) = (x_i, y_i, z_i), x from o1, y from o2, z from o3
                    res = []
                    for i in range(3):
                        res += [o1[i], o2[i], o3[i]]
                    print("Yes")
                    print(" ".join(map(str, res)))
                    return
    print("No")


main()
