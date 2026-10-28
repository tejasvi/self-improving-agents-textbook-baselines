import sys


def main():
    V1, V2, V3 = map(int, sys.stdin.read().split())
    N = 7
    total = 3 * N ** 3
    # Check consistency: V1 + 2*V2 + 3*V3 must equal total volume of 3 cubes.
    if V1 + 2 * V2 + 3 * V3 != total:
        print("No")
        return
    S_target = V2 + 3 * V3  # sum of pairwise intersections
    T_target = V3           # triple intersection

    # Per-axis tuples (L12, L13, L23, L123) for cube 1 at 0, cube 2 at d2, cube 3 at d3.
    R = range(-2 * N, 2 * N + 1)
    tuples = {}
    for d2 in R:
        for d3 in R:
            lo = min(0, d2, d3)
            hi = max(0, d2, d3)
            t = (
                max(0, N - abs(d2)),
                max(0, N - abs(d3)),
                max(0, N - abs(d3 - d2)),
                max(0, N - (hi - lo)),
            )
            if t not in tuples:
                tuples[t] = (d2, d3)
    items = list(tuples.items())

    for t1, o1 in items:
        for t2, o2 in items:
            # partial products over x and y
            p12 = t1[0] * t2[0]
            p13 = t1[1] * t2[1]
            p23 = t1[2] * t2[2]
            p123 = t1[3] * t2[3]
            for t3, o3 in items:
                T = p123 * t3[3]
                if T != T_target:
                    continue
                S = p12 * t3[0] + p13 * t3[1] + p23 * t3[2]
                if S != S_target:
                    continue
                # Found: build full coordinates.
                # cube1 = (0,0,0); cube2 = (o1[0],o2[0],o3[0]); cube3 = (o1[1],o2[1],o3[1])
                c2 = (o1[0], o2[0], o3[0])
                c3 = (o1[1], o2[1], o3[1])
                print("Yes")
                print(0, 0, 0, c2[0], c2[1], c2[2], c3[0], c3[1], c3[2])
                return
    print("No")


main()
