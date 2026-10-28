# Write your solution here. Read from stdin, write to stdout.

import sys

def overlap_len(d):
    # side length L = 7
    L = 7
    return max(0, L - abs(d))

def triple_len(a, b):
    # intervals [0,7], [a, a+7], [b, b+7]
    L = 7
    left = max(0, a, b)
    right = min(L, a + L, b + L)
    return max(0, right - left)

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    V1, V2, V3 = map(int, data)
    L = 7
    cube_volume = L ** 3
    # quick consistency check using derived formula
    # T must satisfy V3 = T and T = (3*L^3 - 2*V2 - V1) / 3
    numerator = 3 * cube_volume - 2 * V2 - V1
    if numerator % 3 != 0:
        print("No")
        return
    T_expected = numerator // 3
    if T_expected != V3:
        print("No")
        return
    # Precompute overlap volume for all possible offsets within [-L, L]
    offsets = []
    vol_map = {}
    for dx in range(-L, L + 1):
        ox = overlap_len(dx)
        for dy in range(-L, L + 1):
            oy = overlap_len(dy)
            for dz in range(-L, L + 1):
                oz = overlap_len(dz)
                vol = ox * oy * oz
                offsets.append((dx, dy, dz, vol))
                vol_map[(dx, dy, dz)] = vol
    # Search for a configuration
    for dx2, dy2, dz2, vol12 in offsets:
        for dx3, dy3, dz3, vol13 in offsets:
            # pair (2,3) offset diff
            diff = (dx2 - dx3, dy2 - dy3, dz2 - dz3)
            vol23 = vol_map.get(diff, 0)
            # triple overlap length per axis
            tx = triple_len(dx2, dx3)
            ty = triple_len(dy2, dy3)
            tz = triple_len(dz2, dz3)
            vol123 = tx * ty * tz
            # compute V2 and V1 from these volumes
            V2calc = vol12 + vol13 + vol23 - 3 * vol123
            V1calc = 3 * cube_volume - 2 * (vol12 + vol13 + vol23) + 3 * vol123
            if V2calc == V2 and V1calc == V1 and vol123 == V3:
                # shift everything to stay within bounds (they already are)
                a1 = b1 = c1 = 0
                a2, b2, c2 = dx2, dy2, dz2
                a3, b3, c3 = dx3, dy3, dz3
                # verify bounds
                if all(abs(v) <= 100 for v in (a1, b1, c1, a2, b2, c2, a3, b3, c3)):
                    print("Yes")
                    print(f"{a1} {b1} {c1} {a2} {b2} {c2} {a3} {b3} {c3}")
                    return
    print("No")

if __name__ == "__main__":
    solve()
