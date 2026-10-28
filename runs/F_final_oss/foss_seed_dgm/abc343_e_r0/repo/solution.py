# Write your solution here. Read from stdin, write to stdout.

import sys

def overlap_len(d):
    d = abs(d)
    return 7 - d if d < 7 else 0

def triple_len(d2, d3):
    lo = max(0, d2, d3)
    hi = min(7, d2 + 7, d3 + 7)
    return hi - lo if hi > lo else 0

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    V1, V2, V3 = map(int, data)
    total = 3 * 7 ** 3  # 1029
    if V1 + 2 * V2 + 3 * V3 != total:
        print("No")
        return
    # Precompute overlap lengths for deltas -7..7
    olap = {d: overlap_len(d) for d in range(-7, 8)}
    # Brute force search over relative positions
    rng = range(-7, 8)
    for dx2 in rng:
        ox12 = olap[dx2]
        for dy2 in rng:
            ox12y = ox12 * olap[dy2]
            for dz2 in rng:
                I12 = ox12y * olap[dz2]
                for dx3 in rng:
                    ox13 = olap[dx3]
                    for dy3 in rng:
                        ox13y = ox13 * olap[dy3]
                        for dz3 in rng:
                            I13 = ox13y * olap[dz3]
                            # pair 2-3 delta
                            dx23 = dx3 - dx2
                            dy23 = dy3 - dy2
                            dz23 = dz3 - dz2
                            I23 = olap[dx23] * olap[dy23] * olap[dz23]
                            # triple intersection
                            T = triple_len(dx2, dx3) * triple_len(dy2, dy3) * triple_len(dz2, dz3)
                            V2calc = I12 + I13 + I23 - 3 * T
                            if V2calc != V2:
                                continue
                            if T != V3:
                                continue
                            # compute V1 for sanity
                            V1calc = total - 2 * V2calc - 3 * T
                            if V1calc != V1:
                                continue
                            # Found solution, output positions (within bounds)
                            a1 = b1 = c1 = 0
                            a2, b2, c2 = dx2, dy2, dz2
                            a3, b3, c3 = dx3, dy3, dz3
                            # ensure within [-100,100]
                            # they already are
                            print("Yes")
                            print(a1, b1, c1, a2, b2, c2, a3, b3, c3)
                            return
    print("No")

if __name__ == "__main__":
    solve()
