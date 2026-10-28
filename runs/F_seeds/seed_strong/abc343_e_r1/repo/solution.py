import sys


def main():
    V1, V2, V3 = map(int, sys.stdin.read().split())
    if V1 + 2 * V2 + 3 * V3 != 3 * 343:
        print("No")
        return
    S = 7

    def ov(ivs):
        lo = max(l for l, _ in ivs)
        hi = min(h for _, h in ivs)
        return max(0, hi - lo)

    # Per-axis overlap signature for offsets (p2, p3) with cube1 at 0.
    # Offsets beyond +-2S can be compressed without changing any overlap.
    seen = {}
    R = range(-2 * S, 2 * S + 1)
    for p2 in R:
        for p3 in R:
            iv = [(0, S), (p2, p2 + S), (p3, p3 + S)]
            key = (ov([iv[0], iv[1]]), ov([iv[0], iv[2]]),
                   ov([iv[1], iv[2]]), ov(iv))
            if key not in seen:
                seen[key] = (p2, p3)
    items = list(seen.items())
    k = len(items)
    target = V2 + 3 * V3

    # Group z-candidates by triple overlap value.
    by_t = {}
    for key, pos in items:
        by_t.setdefault(key[3], []).append((key, pos))

    for i in range(k):
        (x12, x13, x23, x123), (xp2, xp3) = items[i][0], items[i][1]
        for j in range(k):
            (y12, y13, y23, y123), (yp2, yp3) = items[j][0], items[j][1]
            p = x123 * y123
            if p == 0:
                if V3 != 0:
                    continue
                cands = items
            else:
                if V3 % p != 0:
                    continue
                cands = by_t.get(V3 // p, [])
            A = x12 * y12
            B = x13 * y13
            C = x23 * y23
            for (z12, z13, z23, z123), (zp2, zp3) in cands:
                if A * z12 + B * z13 + C * z23 == target and x123 * y123 * z123 == V3:
                    print("Yes")
                    print(0, 0, 0, xp2, yp2, zp2, xp3, yp3, zp3)
                    return
    print("No")


main()
