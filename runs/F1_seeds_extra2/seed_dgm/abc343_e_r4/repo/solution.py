import sys
from itertools import product

L = 7
TOTAL = 3 * L ** 3


def ov(intervals):
    lo = max(s for s, _ in intervals)
    hi = min(e for _, e in intervals)
    return max(0, hi - lo)


def axis_tuples(R):
    """For one axis: cube1 at 0, cube2 at p, cube3 at q.
    Returns dict: (ab, ac, bc, t) -> (p, q) witness."""
    res = {}
    for p, q in product(R, R):
        A = (0, L)
        B = (p, p + L)
        C = (q, q + L)
        key = (ov([A, B]), ov([A, C]), ov([B, C]), ov([A, B, C]))
        if key not in res:
            res[key] = (p, q)
    return res


def solve(V1, V2, V3):
    if V1 + 2 * V2 + 3 * V3 != TOTAL:
        return None
    # Offsets beyond +-2L never create new overlap patterns (gaps >= L suffice).
    R = range(-2 * L - 1, 2 * L + 2)
    tup = axis_tuples(R)
    items = list(tup.items())
    S2 = V2 + 3 * V3
    S3 = V3
    for (kx, wx) in items:
        ax, bx, cx, tx = kx
        for (ky, wy) in items:
            ay, by, cy, ty = ky
            t_xy = tx * ty
            if t_xy == 0:
                if S3 != 0:
                    continue
            elif S3 % t_xy:
                continue
            for (kz, wz) in items:
                az, bz, cz, tz = kz
                if t_xy * tz != S3:
                    continue
                s2 = ax * ay * az + bx * by * bz + cx * cy * cz
                if s2 == S2:
                    p, q = wx
                    r, s = wy
                    u, v = wz
                    return (0, 0, 0, p, r, u, q, s, v)
    return None


def main():
    V1, V2, V3 = map(int, sys.stdin.read().split())
    res = solve(V1, V2, V3)
    if res is None:
        print("No")
    else:
        print("Yes")
        print(*res)


if __name__ == "__main__":
    main()
