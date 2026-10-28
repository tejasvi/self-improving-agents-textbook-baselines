import sys


def main():
    V1, V2, V3 = map(int, sys.stdin.read().split())
    S = 7
    TOTAL = 3 * S ** 3
    if V1 + 2 * V2 + 3 * V3 != TOTAL:
        print("No")
        return

    # Cube 1 is at 0 on each axis; cube 2 and cube 3 start at offsets d2, d3.
    # Per axis, the 1D overlap profile is (L12, L13, L23, L123). Volumes are
    # products of the 1D lengths over the three axes. Keep one representative
    # offset pair (d2, d3) per distinct profile. Offsets beyond +-2S give no
    # new profiles, so the range below is sufficient.
    profiles = {}
    R = range(-2 * S, 2 * S + 1)
    for d2 in R:
        for d3 in R:
            prof = (
                max(0, S - abs(d2)),
                max(0, S - abs(d3)),
                max(0, S - abs(d2 - d3)),
                max(0, min(S, d2 + S, d3 + S) - max(0, d2, d3)),
            )
            if prof not in profiles:
                profiles[prof] = (d2, d3)
    items = list(profiles.items())

    for p1, o1 in items:
        for p2, o2 in items:
            q0 = p1[0] * p2[0]
            q1 = p1[1] * p2[1]
            q2 = p1[2] * p2[2]
            q3 = p1[3] * p2[3]
            for p3, o3 in items:
                T = q3 * p3[3]
                if T != V3:
                    continue
                pair_sum = q0 * p3[0] + q1 * p3[1] + q2 * p3[2]
                if pair_sum - 3 * T != V2:
                    continue
                # Axis k contributes (d2_k, d3_k) = o_k.
                print("Yes")
                print(0, 0, 0,
                      o1[0], o2[0], o3[0],
                      o1[1], o2[1], o3[1])
                return
    print("No")


main()
