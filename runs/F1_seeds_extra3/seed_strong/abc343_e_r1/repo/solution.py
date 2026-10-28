import sys
from collections import defaultdict


def main():
    V1, V2, V3 = map(int, sys.stdin.read().split())
    if V1 + 2 * V2 + 3 * V3 != 3 * 343:
        print("No")
        return
    # per-axis tuples (l12, l13, l23, t) for offsets a1=0, a2, a3
    tuples = set()
    R = range(-14, 15)
    for a2 in R:
        for a3 in R:
            l12 = max(0, 7 - abs(a2))
            l13 = max(0, 7 - abs(a3))
            l23 = max(0, 7 - abs(a2 - a3))
            t = max(0, min(7, a2 + 7, a3 + 7) - max(0, a2, a3))
            tuples.add((l12, l13, l23, t))
    tuples = list(tuples)
    by_t = defaultdict(list)
    for tp in tuples:
        by_t[tp[3]].append(tp)
    target_pair = V2 + 3 * V3
    for x in tuples:
        for y in tuples:
            pxy = x[3] * y[3]
            if pxy == 0:
                if V3 != 0:
                    continue
                cands = tuples
            else:
                if V3 % pxy:
                    continue
                tz = V3 // pxy
                if tz > 7:
                    continue
                cands = by_t.get(tz, [])
            for z in cands:
                p12 = x[0] * y[0] * z[0]
                p13 = x[1] * y[1] * z[1]
                p23 = x[2] * y[2] * z[2]
                if p12 + p13 + p23 == target_pair:
                    # reconstruct offsets: a1=0, a2, a3 from tuples
                    sol = find_offsets(x, y, z)
                    print("Yes")
                    print(" ".join(map(str, sol)))
                    return
    print("No")


_cache = {}


def offsets_for(tp):
    if tp in _cache:
        return _cache[tp]
    for a2 in range(-14, 15):
        for a3 in range(-14, 15):
            l12 = max(0, 7 - abs(a2))
            l13 = max(0, 7 - abs(a3))
            l23 = max(0, 7 - abs(a2 - a3))
            t = max(0, min(7, a2 + 7, a3 + 7) - max(0, a2, a3))
            if (l12, l13, l23, t) == tp:
                _cache[tp] = (a2, a3)
                return (a2, a3)
    raise RuntimeError


def find_offsets(x, y, z):
    ax = offsets_for(x)
    ay = offsets_for(y)
    az = offsets_for(z)
    # cube i coordinates: (0, a2, a3) per axis for cubes 1,2,3
    a1 = (0, 0, 0)
    c2 = (ax[0], ay[0], az[0])
    c3 = (ax[1], ay[1], az[1])
    return [a1[0], a1[1], a1[2], c2[0], c2[1], c2[2], c3[0], c3[1], c3[2]]


main()
