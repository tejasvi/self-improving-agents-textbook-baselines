import sys


def build_axis_patterns():
    # Cube 1 occupies [0,7] on this axis; cubes 2 and 3 start at u and v.
    # Record (overlap12, overlap13, overlap23, overlap123) with a representative (u, v).
    pats = {}
    R = range(-14, 15)
    for u in R:
        for v in R:
            p12 = max(0, 7 - abs(u))
            p13 = max(0, 7 - abs(v))
            p23 = max(0, 7 - abs(u - v))
            t = max(0, min(7, u + 7, v + 7) - max(0, u, v))
            key = (p12, p13, p23, t)
            if key not in pats:
                pats[key] = (u, v)
    return pats


def solve(V1, V2, V3):
    if V1 + 2 * V2 + 3 * V3 != 1029:
        return None
    pats = build_axis_patterns()
    D = list(pats.items())  # (key, (u, v))
    byT = {}
    for idx, (key, _) in enumerate(D):
        byT.setdefault(key[3], []).append(idx)
    S2 = V2 + 3 * V3
    S3 = V3
    n = len(D)
    for i in range(n):
        k1, r1 = D[i]
        a12, a13, a23, t1 = k1
        for j in range(n):
            k2, r2 = D[j]
            b12, b13, b23, t2 = k2
            tt = t1 * t2
            if tt == 0:
                if S3 != 0:
                    continue
                cands = range(n)
            else:
                if S3 % tt != 0:
                    continue
                need = S3 // tt
                cands = byT.get(need, [])
            for m in cands:
                k3, r3 = D[m]
                c12, c13, c23, t3 = k3
                if t1 * t2 * t3 != S3:
                    continue
                s2 = a12 * b12 * c12 + a13 * b13 * c13 + a23 * b23 * c23
                if s2 != S2:
                    continue
                # Axis tuples: cube1 origin, cube2 = (r1.u, r2.u, ...) careful below
                # Per axis: cube2 offset = r[0], cube3 offset = r[1]
                return [
                    0, 0, 0,
                    r1[0], r2[0], r3[0],
                    r1[1], r2[1], r3[1],
                ]
    return None


def main():
    V1, V2, V3 = map(int, sys.stdin.read().split())
    res = solve(V1, V2, V3)
    if res is None:
        print("No")
    else:
        print("Yes")
        print(" ".join(map(str, res)))


if __name__ == "__main__":
    main()
