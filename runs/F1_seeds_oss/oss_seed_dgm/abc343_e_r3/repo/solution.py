# Write your solution here. Read from stdin, write to stdout.

import sys

def overlap_len(d: int) -> int:
    """Return length of overlap between intervals [0,7] and [d, d+7]."""
    d = abs(d)
    return max(0, 7 - d)

def triple_len(a: int, b: int) -> int:
    """Length of intersection of three intervals [0,7], [a,a+7], [b,b+7]."""
    left = max(0, a, b)
    right = min(7, a + 7, b + 7)
    return max(0, right - left)

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    V1, V2, V3 = map(int, data)
    TOTAL = 3 * 7 * 7 * 7  # total volume of three cubes counted with multiplicity
    # Necessary condition from inclusion–exclusion
    if V1 + 2 * V2 + 3 * V3 != TOTAL:
        print("No")
        return

    # Pre‑compute per‑dimension data for offsets of cube2 and cube3 relative to cube1 (placed at origin).
    rng = range(-7, 8)  # offsets where overlap may be non‑zero; offset = 7 also gives zero overlap which is enough.
    dim_items = []  # each element: (dx2, dx3, ox12, ox13, ox23, tx)
    for dx2 in rng:
        ox12 = overlap_len(dx2)
        for dx3 in rng:
            ox13 = overlap_len(dx3)
            ox23 = overlap_len(dx3 - dx2)
            tx = triple_len(dx2, dx3)
            dim_items.append((dx2, dx3, ox12, ox13, ox23, tx))

    # Combine x and y dimensions first (store intermediate products).
    xy_combos = []  # each: (vol12_xy, vol13_xy, vol23_xy, triple_xy, dx2x, dx3x, dx2y, dx3y)
    for (dx2x, dx3x, ox12x, ox13x, ox23x, txx) in dim_items:
        for (dx2y, dx3y, ox12y, ox13y, ox23y, txy) in dim_items:
            vol12_xy = ox12x * ox12y
            vol13_xy = ox13x * ox13y
            vol23_xy = ox23x * ox23y
            triple_xy = txx * txy
            xy_combos.append((vol12_xy, vol13_xy, vol23_xy, triple_xy,
                               dx2x, dx3x, dx2y, dx3y))

    # Now iterate over z dimension and try to match the required V2 and V3.
    for (dx2z, dx3z, ox12z, ox13z, ox23z, txz) in dim_items:
        for (vol12_xy, vol13_xy, vol23_xy, triple_xy,
             dx2x, dx3x, dx2y, dx3y) in xy_combos:
            vol12 = vol12_xy * ox12z
            vol13 = vol13_xy * ox13z
            vol23 = vol23_xy * ox23z
            V3calc = triple_xy * txz
            V2calc = vol12 + vol13 + vol23 - 3 * V3calc
            if V2calc == V2 and V3calc == V3:
                # Found a solution.
                print("Yes")
                print(f"0 0 0 {dx2x} {dx2y} {dx2z} {dx3x} {dx3y} {dx3z}")
                return
    print("No")

if __name__ == "__main__":
    solve()
